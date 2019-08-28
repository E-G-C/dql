

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
