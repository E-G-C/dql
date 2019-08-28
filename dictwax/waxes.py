from dataclasses import dataclass
from typing import Any


@dataclass(eq=False, order=False)
class RepWax:
    """Replacement Wax class"""
    targets: dict = None


@dataclass(eq=False, order=False)
class RemWax:
    """Removal Wax class"""
    targets: list = None


@dataclass(eq=False, order=False)
class WaxOn:
    value: Any = None
    wax: [RepWax or RemWax] = None


def waxoff(source_dict: dict, waxed_dict) -> dict:
    """Wax On, Wax Off :)
    Used to map one dictionary into another in the form of
    ::
           source_dict              waxed_dict                  clean dict
        {                                                {
          'key1':'key1_value',+---------------------->      'some_other_key3' : 'key1_value',
          'key2':'key2_value' +---------------------->      'some_other_key3' : 'key2_value'
        }                                                }

    :param source_dict: original dict to be applied wax on
            example::
                {
                    'key1':'key1_value'
                    'key2':'key2_value'
                }

    :param waxed_dict: dictionary with waxed values
            example::
              {
                'some_other_key3' : MapItem(['key1'])',
                'some_other_key4' : MapItem(['key2'], Patch(['unwanted'], 'unwanted replacement')),'
              }

    :return: a new dictionary with cleaned items
    """

    def _search_for_wax(value):
        if isinstance(value, dict):
            for k in list(value.keys()):
                if isinstance(value[k], dict) or isinstance(value[k], list):
                    _search_for_wax(value[k])
                else:
                    _apply_wax(k, value)
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict) or isinstance(item, list):
                    _search_for_wax(item)
                else:
                    _apply_wax(i, value)

    def _apply_wax(k, value):
        if isinstance(value[k], WaxOn):
            _wax_item = value[k]
            item_value = _wax_item.value
            value[k] = item_value
            if _wax_item.wax and item_value in _wax_item.wax.targets:
                if isinstance(_wax_item, RepWax):
                    value[k] = _wax_item.wax.targets[item_value]
                    return
                elif isinstance(_wax_item, RemWax):
                    value.pop(k)
                    return
            if item_value:
                value[k] = item_value

    _search_for_wax(waxed_dict)
    return waxed_dict
