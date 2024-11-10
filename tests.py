import unittest
from conf_parser import parse_dict, parse_value

class TestConfParser(unittest.TestCase):

    def parse_dict_test(self):
        self.assertEqual(parse_dict('{a => 1, b => 2}', {}), {'a': 1, 'b': 2})

    def parse_value_test(self):
        self.assertEqual(parse_value('1', {}), 1)
        self.assertEqual(parse_value('1.0', {}), 1.0)
        self.assertEqual(parse_value('{a => 1, b => 2}', {}), {'a': 1, 'b': 2})
        self.assertEqual(parse_value('!a', {'a': 1}), 1)