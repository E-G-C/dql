# ---------------------------------
#          Utils
# -------------------------------


def json_path_to_dict_path(json_path: str):
    map_reference = json_path.replace('[', '.')
    map_reference = map_reference.replace(']', '')

    dict_path = map_reference.split('.')

    for i in range(len(dict_path)):
        dict_path[i] = int(dict_path[i]) if dict_path[i].isdigit() else dict_path[i]

    return dict_path


def dig(your_dict, *keys):
    """digs into an dict, if anything along the way is None, then simply return None
    """
    end_of_chain = your_dict
    key_present = True
    for key in keys:
        if (isinstance(end_of_chain, dict) and (key in end_of_chain)) or (
                isinstance(end_of_chain, (list, tuple)) and isinstance(key, int)):
            try:
                end_of_chain = end_of_chain[key]
            except IndexError:
                return None
        else:
            key_present = False

    return end_of_chain if key_present else None


# ----------------------------------------------------------------
#               Where related methods
# ----------------------------------------------------------------
def _where_bool_(instance):
    """Used for truth value testing"""
    return True if instance.source else False


def _get_where_result(instance, condition):
    """Executes the condition against the given instance.source value,
     this must be a valid Python sentence
     """
    if not instance.source:
        return None
    if isinstance(instance.source, (str, int, bool)):
        if eval(condition, {}, {instance.selection[0]: instance.source}):
            return instance.source
        else:
            return None
    if isinstance(instance.source, dict):
        return get_sub_dict(instance.source, instance.selection, condition)
    if isinstance(instance.source, list):
        return get_sub_list(instance.source, instance.selection, instance.path, condition)

    raise Exception('Unsupported type')


# ----------------------------------------------------------------
#          "From" and "Select" common methods
# ----------------------------------------------------------------
def eval_condition(condition, locals):
    """Evaluates the condition, if a given variable used in the condition
    isn't present, it defaults it to None
    """
    import ast
    condition_variables = set()
    st = ast.parse(condition)
    for node in ast.walk(st):
        if type(node) is ast.Name:
            condition_variables.add(node.id)
    for v in condition_variables:
        if v not in locals:
            locals[v] = None
    result = eval(condition, {}, locals)
    return result


def get_sub_list(source, selection, path, condition='True'):
    """Applies the condition against a list, producing a new list with
    the values that match the condition. the list can be made up of dictionaries
     """
    result = []
    if condition is None:
        if selection[0] == '*':
            return source
        else:
            condition = 'True'
    if isinstance(source[0], (int, str, bool)):
        selection = path[-1] if selection[0] == '*' else selection
        result = [v for v in source if eval_condition(condition, {selection[0]: v})]
    elif isinstance(source[0], dict):
        for d in source:
            new_item = get_sub_dict(d, selection, condition)
            if new_item: result.append(new_item)
    return result


def get_sub_dict(source, selection, condition='True'):
    """
    Applies the condition to dictionary values
    :param source: dictionary to apply the condition
    :param selection: keys to extract from source dictionary
    :param condition: condition to apply
    :return: either the original dictionary or a new dictionary
    with the extracted keys
    """

    if condition is None:
        if selection[0] == '*':
            return source
        else:
            condition = 'True'
    result = None
    if selection[0] == '*':
        selection = source.keys()

    if eval_condition(condition, source):

        result = {k: v for (k, v) in source.items() if (k in selection)}
        for missing_key in selection:
            if missing_key not in result.keys():
                result[missing_key] = None
    return result


# ----------------------------------------------------------------
#     End of common methods
# ----------------------------------------------------------------

class _From:
    """
    json path to the json element to query from.
    """

    def __call__(self):
        if self.path:
            result = dig(self.source, *self.path)
        else:
            result = self.source

        if not result:
            #  Mock a result to be able to create a Where
            result = ''

        from_result = self._get_from_result(result)

        Where = type('WhereClause', (result.__class__,),
                     dict(source=result, selection=self.selection,
                          path=self.path,
                          Where=_get_where_result,
                          w=_get_where_result, __bool__=_where_bool_))
        ql_result = Where(from_result)
        return ql_result

    def _get_from_result(self, source):
        """Executes the condition against the given instance.source value,
         this must be a valid Python sentence
         """
        if not source:
            return None
        if isinstance(source, (str, int, bool)):
            return source
        if isinstance(source, dict):
            return get_sub_dict(source, self.selection)
        if isinstance(source, list):
            return get_sub_list(source, self.selection, self.path)

        raise Exception('Unsupported type')


class DictQL:
    """Allows to query a dictionary (based on a json file) to be queried
    sql-like style.
    :param Select:  string, either '*' indicating all the fields or comma
    separated field names
    :param From:  string, the path to the element to be queried.
    :param Where: string, optional, represents a valid Python expression
    to be evaluated
    example
    ::

        # descriptive names
        from dql import DictQL
        # or shorthanded version
        from dql import Dql

        source = {
                "a":      1,
                "b":      2,
                "c":      [
                        {
                                "d0": 5,
                                "d1": 10,
                                "d2": 15
                        },
                        {
                                "d4": 4,
                                "d5": 20,
                                "d6": 50
                        }
                ],
                "nested": {
                        "e": 5,
                        "f": "6",
                        "g": {"k": 100, "l": 200, "m": 300}
                },
                "j":      [1, 2, 3, 4, 5, 6, 7, 8, 9]
        }

        single_element = DictQL(source).Select('b').From('b')
        print(f'Single element {single_element}')

        partial_dict = DictQL(source).Select('d0,d2').From('c')
        print(f'partial dict: {partial_dict}')

        full_dict = DictQL(source).Select('*').From('nested.g').Where('l==200')
        print(f'full dict {full_dict}')

        # shorthanded space saving
        list_elements = Dql(source).s('*').f('j').w('j>4')
        print(f'Filtered list {list_elements}')

    """

    def __init__(self, source):
        """
        :param source: dictionary to be queried
        """
        self.target = []
        self.source = source
        self.s = self.Select
        self.f = self.From

    def Select(self, target):
        self.target = list(map(lambda x: x.strip(), target.split(',')))
        return self

    def From(self, *path):
        _from = _From()
        _from.source = self.source
        _from.selection = self.target

        _from.path = json_path_to_dict_path(path[0])
        return _from()
