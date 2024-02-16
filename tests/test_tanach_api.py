import unittest
import re
from ..src.sefaria_api import _replace_panctuation_series, _remove_footnotes, _remove_non_hebrew_letters, _remove_empty_parentheses

class TestReplacePanctuationSeries(unittest.TestCase):
    def test_replace_panctuation_series(self):
        text = 'Hello... world!'
        expected_output = 'Hello. world!'
        self.assertEqual(_replace_panctuation_series(text), expected_output)

        text = 'This is a test---'
        expected_output = 'This is a test-'
        self.assertEqual(_replace_panctuation_series(text), expected_output)

        text = 'No panctuation here'
        expected_output = 'No panctuation here'
        self.assertEqual(_replace_panctuation_series(text), expected_output)

        text = 'Multiple,,,.,, commas'
        expected_output = 'Multiple, commas'
        self.assertEqual(_replace_panctuation_series(text), expected_output)

        text = 'Multiple... periods'
        expected_output = 'Multiple. periods'
        self.assertEqual(_replace_panctuation_series(text), expected_output)

        text = 'Multiple--- dashes'
        expected_output = 'Multiple- dashes'
        self.assertEqual(_replace_panctuation_series(text), expected_output)

        text = 'Multiple... periods and,,, commas'
        expected_output = 'Multiple. periods and, commas'
        self.assertEqual(_replace_panctuation_series(text), expected_output)

        text = 'Multiple combined panctuation...,,,---' 
        expected_output = 'Multiple combined panctuation.'
        self.assertEqual(_replace_panctuation_series(text), expected_output)

class TestRemoveFootnotes(unittest.TestCase):
    def test_remove_footnotes(self):
        text = 'This is a test with <sup class="footnote-marker">1</sup><i class="footnote">Footnote 1</i> footnotes.'
        expected_output = 'This is a test with  footnotes.'
        self.assertEqual(_remove_footnotes(text), expected_output)

        text = 'No footnotes here'
        expected_output = 'No footnotes here'
        self.assertEqual(_remove_footnotes(text), expected_output)

        text = 'Multiple footnotes <sup class="footnote-marker">1</sup><i class="footnote">Footnote 1</i> <sup class="footnote-marker">2</sup><i class="footnote">Footnote 2</i>'
        
        expected_output = 'Multiple footnotes '
        self.assertEqual(_remove_footnotes(text).strip(), expected_output.strip())

class TestRemoveNonHebrewLetters(unittest.TestCase):
    def test_remove_non_hebrew_letters(self):
        text = 'שלום! Hello! 123'
        expected_output = 'שלום  '
        self.assertEqual(_remove_non_hebrew_letters(text).strip(), expected_output.strip())

        text = 'אבגדהוזחטיכלמנסעפצקרשת'
        expected_output = 'אבגדהוזחטיכלמנסעפצקרשת'
        self.assertEqual(_remove_non_hebrew_letters(text), expected_output)

        text = 'This is a test'
        expected_output = ''
        self.assertEqual(_remove_non_hebrew_letters(text).strip(), expected_output)


class TestRemoveEmptyParentheses(unittest.TestCase):
    def test_remove_empty_parentheses(self):
        text = 'Hello () world!'
        expected_output = 'Hello world!'
        self.assertEqual(_remove_empty_parentheses(text), expected_output)

        text = 'This is a test (   )'
        expected_output = 'This is a test '
        self.assertEqual(_remove_empty_parentheses(text), expected_output)

        text = 'No parentheses here'
        expected_output = 'No parentheses here'
        self.assertEqual(_remove_empty_parentheses(text), expected_output)

        text = 'Multiple () () parentheses'
        expected_output = 'Multiple  parentheses'
        self.assertEqual(_remove_empty_parentheses(text), expected_output)

        text = 'Multiple (   ) (   ) parentheses'
        expected_output = 'Multiple  parentheses'
        self.assertEqual(_remove_empty_parentheses(text), expected_output)

if __name__ == '__main__':
    unittest.main()