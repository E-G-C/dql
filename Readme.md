## DictQL
Allows to run python expression against dictionary's values, kind of sql a query. I built it for dictionaries based on a json files. 
QuickStart: Create an instance of DictQL passing in a dictionary
```foo = DictQL(my_dict)```
then 'query' the value of your element passing in the json-path (dot notation)  


* `Select`:  string, either '*' indicating all the fields or a list of fields.
* `From`:  string, the json-path to the element to be queried, or From() to query the dict itself.
* `Where`: string, optional, represents a valid Python expression to be evaluated.



See bellow, more examples can be fund in the [test file](dql/test_dictQL.py):
```

from dql import DictQL

import json

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

source_ql = DictQL(source)


print('-'*20)
print('Single element')
single_element_1 = source_ql.Select('b').From('b')
print(f"source_ql.Select('b').From('b')={single_element_1}")
# equivalent to
print(f"this is equivalent to:")
single_element_2 = source_ql.s('*').From('b')
print(f"source_ql.Select('*').From('b')={single_element_2}")

print('-'*20)
print('Sub Dic ')
partial_dict = source_ql.Select('d0, d2').From('c')
print(f'List of sub dictionaries: {json.dumps(partial_dict)}')

print('-'*20)
print('Full and nested Dic ')
full_dict = source_ql.Select('*').From('nested.g')
print(f'full dict {json.dumps(full_dict)}')

print('-'*20)
print('Full List ')
full_list = source_ql.Select('*').From('j')
print(f'j= {full_list}')

print('-'*20)
print('Filtered List ')
print(full_list.Where('j==3'))

# space saving
list_elements = source_ql.s('*').f('j').w('j>4')
print(f'Filtered list {list_elements}')

no_elements = source_ql.s('*').f('po')
print(no_elements)

if no_elements:
    print('got something back')
else:
    print('got nothing back')


print('-'*20)
print('Key aliases ')

x = source_ql.Select('a as "this used to be a", b as y, j as z').From()
print(x)



print('-'*20)
print('Constants ')

cons1 = source_ql.Select('constant_name: 2, b as y').From()
print(cons1)

cons2 = source_ql.Select('b:4, b as y, 3:$').From()
print(cons2)

    
```
