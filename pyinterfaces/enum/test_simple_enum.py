"""
"""
from __future__ import absolute_import

import unittest

from . import simple_enum as enum



HOSTS = enum.Enumerant()
HOSTS.THEATLANTIC = enum.RegexCase('github.com/theatlantic')
HOSTS.PYPI = enum.RegexCase('pypi.python.org')
HOSTS.default = enum.RegexCase('*')


NOFALLBACK = enum.Enumerant()
NOFALLBACK.THEATLANTIC = enum.RegexCase('github.com/theatlantic')
NOFALLBACK.PYPI = enum.RegexCase('pypi.python.org')


class EnumerantTests(unittest.TestCase):
    def test_example(self):
        urls = {
            'ours': 'https://github.com/theatlantic/python-ldap',
            'pypi': 'https://pypi.python.org/pypi/pytz/',
            'other':'https://github.com/python-pillow/Pillow'
        }

        self.assertEqual(HOSTS.match(urls['ours']), HOSTS.THEATLANTIC)
        self.assertEqual(HOSTS.match(urls['pypi']), HOSTS.PYPI)

        thing = urls['other']
        print()
        print("thing:", type(thing), thing)
        print()
        import pdb
        pdb.set_trace()
        print()
        

        self.assertEqual(HOSTS.match(urls['other']), HOSTS.default)

    def test_classproperties(self):
        self.assertEqual(set(HOSTS.cases), set([HOSTS.THEATLANTIC, HOSTS.PYPI]))
        self.assertEqual(set([HOSTS.default]), set([HOSTS.FALLBACK]))        

    def test_exceptions(self):
        self.assertRaises(enum.EnumerantMatchError, lambda: NOFALLBACK.match('zzzzz'))


if __name__ == "__main__":
    unittest.main()
