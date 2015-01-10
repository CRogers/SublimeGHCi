import unittest
from unittest.mock import *

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.completions.TypeAddingCompletor import *

class Completor(object):
    def __init__(self):
        self.complete = Mock(return_value=[])

class ExtraGhciCommands(object):
    def __init__(self):
        self.name_to_type_or_kind = dict()
    
    def type_or_kind_of(self, expr):
        if expr in self.name_to_type_or_kind:
            return Fallible.succeed(self.name_to_type_or_kind[expr])
        else:
            return Fallible.fail('failed')

s = Fallible.succeed

class TypeAddingCompletorSpec(unittest.TestCase):
    def setUp(self):
        self.completor = Completor()
        self.ghci_commands = ExtraGhciCommands()
        self.type_adding_completor = TypeAddingCompletor(self.completor, self.ghci_commands)

    def test_when_underlying_completor_returns_no_results_return_no_results(self):
        completions = self.type_adding_completor.complete_with_types('abc', 3)
        self.assertEqual(completions, [])

    def test_when_underlying_completor_returns_one_result_return_that_result_and_its_type(self):
        self.ghci_commands.name_to_type_or_kind = {'yay': 'sometype'}
        self.completor.complete.return_value = ['yay']
        completions = self.type_adding_completor.complete_with_types('abc', 3)
        self.assertEqual(completions, [('yay', s('sometype'))])

    def test_when_underlying_completor_returns_two_results_it_returns_those_results_and_their_types(self):
        self.ghci_commands.name_to_type_or_kind = {'yay': 'sometype', 'foo': 'bar'}
        self.completor.complete.return_value = ['yay', 'foo']
        completions = self.type_adding_completor.complete_with_types('abc', 3)
        self.assertEqual(completions, [('yay', s('sometype')), ('foo', s('bar'))])