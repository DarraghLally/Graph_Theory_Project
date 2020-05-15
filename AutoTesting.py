# For testing
import unittest

# Bringing in match function from regex.py
from regex import match

"""Class AutoTesting

Main mane option to run automated testing with hard-coded
for both the regular expression and string for testing.
"""
class AutoTesting(unittest.TestCase):

    def test_and_or(self):
        self.assertTrue(match("a.b|b*", "bbbbb"))
        self.assertFalse(match("a.b|b*", "bbbbbn"))

    def test_and(self):
        self.assertTrue(match("a.b", "ab"))
        self.assertFalse(match("a.b", "c"))

    def test_or(self):
        self.assertTrue(match("c|a", "c"))
        self.assertFalse(match("c|a", "b"))

    def test_any_num(self):
        self.assertTrue(match("b*", ""))
        self.assertFalse(match("b**", "bbbbbb"))

    def test_one_more(self):
        self.assertTrue(match("b+", "bbb"))
        self.assertFalse(match("b+", ""))

    def test_zero_one():
        self.assertTrue(match("c?", ""))
        self.assertFalse(match("c?", "aa"))

    