import unittest
from unittest.mock import *

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.completions.OutputCompletor import *
	
class TypedCompletor(object):
	def __init__(self):
		self.complete_with_types = Mock(return_value=[])

class OutputCompletorSpec(unittest.TestCase):
	def setUp(self):
		self.completor = TypedCompletor()
		self.output_completor = OutputCompletor(self.completor)

	def test_if_the_underlying_completor_returns_no_results_it_should_return_no_results(self):
		completions = self.output_completor.complete('abc', 3)
		self.assertEqual(completions, [])

	def test_if_the_underlying_completor_returns_one_result_with_type_it_formats_it_correctly(self):
		self.completor.complete_with_types.return_value = [('foo', Fallible.succeed('bar'))]
		completions = self.output_completor.complete('abc', 3)
		self.assertEqual(completions, [('foo\tbar', 'foo')])

	def test_if_the_underlying_completor_returns_two_results_with_types_it_formats_them_correctly(self):
		self.completor.complete_with_types.return_value = [('foo', Fallible.succeed('bar')), ('abc', Fallible.succeed('def'))]
		completions = self.output_completor.complete('abc', 3)
		self.assertEqual(completions, [('foo\tbar', 'foo'), ('abc\tdef', 'abc')])