from unittest import TestCase
import json
from dictQL import DictQL


class DictQL_test(TestCase):
    def setUp(self) -> None:
        with open('test_file.json') as _:
            self.source = json.load(_)
        # print(json.dumps(self.source))

    def test_root_single_element(self):
        actual = DictQL(self.source).Select('a').From('a')
        self.assertEqual(actual, 1)

    def test_root_list(self):
        actual = DictQL(self.source).Select('j').From('j')
        self.assertTrue(hasattr(actual, '__len__'))

    def test_single_element_Where(self):
        actual_None = DictQL(self.source).Select('b').From('b').Where('b<1')
        self.assertIsNone(actual_None)
        actual_last = DictQL(self.source).Select('z').From('z').Where('z=="last"')
        self.assertEqual(actual_last, 'last')

    def test_nested_element_from_array(self):
        actual = DictQL(self.source).Select('*').From('j').Where('j>3')
        expected = [4, 5, 6, 7, 8, 9]
        self.assertEqual(actual.sort(), expected.sort())

    def test_pulling_elements_from_dict(self):
        dd2 = DictQL(self.source).Select('source,d2').From('g.c').Where('source==10')
        self.assertEqual(dd2, [])

        actual_list = DictQL(self.source).Select('source,d6').From('g.c').Where('source==None')
        actual_dict = actual_list[0]
        print(actual_list)
        expected_dict = {'d6': 50, 'source': None}

        same_items = {k: actual_dict[k] for k in actual_dict if
                      k in expected_dict and actual_dict[k] == expected_dict[k]}
        self.assertEqual(len(same_items), 2)

        actual_list2 = DictQL(self.source).Select('d1').From('g.c').Where('source==5 or source=="5"')
        print(actual_list2)
