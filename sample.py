# from dql import DictQL
from dql import DictQL
# shorthanded version
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

full_list = DictQL(source).Select('*').From('j')
print(f'Full list {full_list}')


# space saving
list_elements = Dql(source).s('*').f('j').w('j>4')
print(f'Filtered list {list_elements}')

