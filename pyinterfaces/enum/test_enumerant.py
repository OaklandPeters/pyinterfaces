"""
"""
from __future__ import absolute_import

import unittest

from . import enumerant as enum


class Host(enum.RegexCase):
    pass


class HOSTS(enum.Enumerant):
    THEATLANTIC = Host('github.com/theatlantic')
    PYPI = Host('pypi.python.org')
    FALLBACK = Host('*')

class NOFALLBACK(enum.Enumerant):
    THEATLANTIC = Host('github.com/theatlantic')
    PYPI = Host('pypi.python.org')


class EnumerantTests(unittest.TestCase):


    def test_example(self):
        urls = {
            'ours': 'https://github.com/theatlantic/python-ldap',
            'pypi': 'https://pypi.python.org/pypi/pytz/',
            'other':'https://github.com/python-pillow/Pillow'
        }

        self.assertEqual(HOSTS.match(urls['ours']), HOSTS.THEATLANTIC)
        self.assertEqual(HOSTS.match(urls['pypi']), HOSTS.PYPI)
        self.assertEqual(HOSTS.match(urls['other']), HOSTS.FALLBACK)

    def test_classproperties(self):
        self.assertEqual(set(HOSTS.cases), set([HOSTS.THEATLANTIC, HOSTS.PYPI]))
        self.assertEqual(set([HOSTS.default]), set([HOSTS.FALLBACK]))        

    def test_exceptions(self):
        self.assertRaises(enum.EnumerantMatchError, lambda: NOFALLBACK.match('zzzzz'))


if __name__ == "__main__":
    unittest.main()
