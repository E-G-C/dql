from dataclasses import dataclass
from typing import Any


def json_path_to_dict_path(json_path: str):
    map_reference = json_path.replace('[', '.')
    map_reference = map_reference.replace(']', '')

    dict_path = map_reference.split('.')

    for i in range(len(dict_path)):
        dict_path[i] = int(dict_path[i]) if dict_path[i].isdigit() else dict_path[i]

    return dict_path


@dataclass(eq=False, order=False)
class Patch:
    target: list = None
    replacement: str = None


@dataclass(eq=False, order=False)
class MapItem:
    value: Any = None
    allow_empty: bool = True
    allow_null: bool = True
    patch: Patch = None


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


def transform(source_dict: dict, map_definition) -> dict:
    """Used to map one dictionary into another in the form of
    ::
           source_dict           map_definitions               outcome
        {                                                {
          'key1':'key1_value',+---------------------->      'some_other_key3' : 'key1_value',
          'key2':'key2_value' +---------------------->      'some_other_key3' : 'key2_value'
        }                                                }

    :param source_dict: original dict to be transformed according the map_definitions dictionary
            example::
                {
                    'key1':'key1_value'
                    'key2':'key2_value'
                }

    :param map_definition: dictionary describing the source_dict transformations
            example::
              {
                'some_other_key3' : MapItem(['key1'])',
                'some_other_key4' : MapItem(['key2'], Patch(['unwanted'], 'unwanted replacement')),'
              }

    :return: a new dictionary result of applying the map_definition
    """

    def explore(value):
        if isinstance(value, dict):
            for k in list(value.keys()):
                if isinstance(value[k], dict) or isinstance(value[k], list):
                    explore(value[k])
                else:
                    check_for_map_item(k, value)
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict) or isinstance(item, list):
                    explore(item)
                else:
                    check_for_map_item(i, value)

    def check_for_map_item(k, value):
        if isinstance(value[k], MapItem):
            _map_item = value[k]
            item_value = _map_item.value
            value[k] = item_value
            if _map_item.patch and _map_item.patch.target and item_value in _map_item.patch.target:
                value[k] = _map_item.patch.replacement
            if item_value == '' and not _map_item.allow_empty:
                value.pop(k)
            if (item_value is None) and not _map_item.allow_null:
                value.pop(k)
            if item_value:
                value[k] = item_value

    explore(map_definition)
    return map_definition


if __name__ == '__main__':
    # b = {'b': 'b-value', 'c': 'c-value'}
    # a = {'a': MapItem(None, allow_null=False)}
    # source = transform(b, a)
    # print(source)
    c =  json_path_to_dict_path('g.c[1]')
    print (c)
