import unittest
from unittest.mock import *

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.completions.TypeMatchingCompletor import *

class Sublime(object):
	def Region(self, start, end):
		return (start, end)

class TypedCompletor(object):
	def __init__(self):
		self.complete_with_types = Mock(return_value = [])

class TypeHoleInfoExtractor(object):
	def __init__(self):
		self.type_at_point = Mock(return_value = Fallible.fail(None))

class View(object):
	def __init__(self):
		self.text = 'test'

	def substr(self, range):
		return 'blah'

	def size(self):
		return 10

class TypeMatchingCompletorSpec(unittest.TestCase):
	def setUp(self):
		self.view = View()
		self.completor = TypedCompletor()
		self.info_extractor = TypeHoleInfoExtractor()
		self.type_matching_completor = TypeMatchingCompletor(Sublime(), self.completor, self.info_extractor, self.view)

	def test_when_there_are_no_completions_then_no_completions_are_produced(self):
		result = self.type_matching_completor.complete_with_types('', 4)
		self.assertEqual(result, [])

	def test_when_the_type_extractor_fails_the_same_completions_are_returned(self):
		completions = [('f', 'a'), ('g', 'b')]
		self.completor.complete_with_types.return_value = completions
		result = self.type_matching_completor.complete_with_types('', 4)
		self.assertEqual(result, completions)

	def test_when_there_are_two_completions_and_the_first_is_equal_to_the_type_at_cursor_put_that_one_on_top(self):
		completions = [('f', 'a'), ('g', 'b')]
		self.completor.complete_with_types.return_value = completions
		self.info_extractor.type_at_point.return_value = Fallible.succeed('a')
		result = self.type_matching_completor.complete_with_types('', 4)
		self.assertEqual(result, completions)

	def test_when_there_are_two_completions_and_the_last_is_equal_to_the_type_at_cursor_put_that_one_on_top(self):
		self.completor.complete_with_types.return_value = [('f', 'a'), ('g', 'b')]
		self.info_extractor.type_at_point.return_value = Fallible.succeed('b')
		result = self.type_matching_completor.complete_with_types('', 4)
		self.assertEqual(result, [('g', 'b'), ('f', 'a')])

	def test_when_there_are_three_completions_and_the_last_two_are_equal_to_the_type_at_cursor_put_those_two_on_top(self):
		self.completor.complete_with_types.return_value = [('f', 'a'), ('g', 'b'), ('h', 'b')]
		self.info_extractor.type_at_point.return_value = Fallible.succeed('b')
		result = self.type_matching_completor.complete_with_types('', 4)
		self.assertEqual(result, [('g', 'b'), ('h', 'b'), ('f', 'a')])

