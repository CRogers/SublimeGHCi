import unittest
from unittest.mock import *

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.completions.Completor import *

class GhciCommands(object):
    pass
    
class CompletorSpec(unittest.TestCase):
    def setUp(self):
        self.commands = GhciCommands()
        self.commands.completions = Mock(return_value=Fallible.succeed([]))
        self.completor = Completor(self.commands)

    def test_when_completions_returns_nothing_complete_returns_nothing(self):
        completed = self.completor.complete('abc', 2)
        self.assertEqual(completed, [])

    def test_when_completions_fails_complete_returns_nothing(self):
        self.commands.completions.return_value = Fallible.fail('failed')
        completed = self.completor.complete('abc', 2)
        self.assertEqual(completed, [])

    def test_when_completions_returns_a_value_complete_returns_it(self):
        self.commands.completions.return_value = Fallible.succeed(['abc'])
        completed = self.completor.complete('a', 2)
        self.assertEqual(completed, ['abc'])

    def test_when_the_location_is_the_beginning_of_the_file_it_works(self):
        completed = self.completor.complete('abc', 0)
        self.assertEqual(completed, [])