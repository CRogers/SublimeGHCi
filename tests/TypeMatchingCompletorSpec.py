import unittest
from unittest.mock import *

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.completions.TypeMatchingCompletor import *

class Sublime(object):
	def Region(self, start, end):
		return (start, end)

class ExtraGhciCommands(object):
	def __init__(self):
		self.supertypes = []

	def is_supertype_of(self, subtype, supertype):
		return (subtype == supertype) or (subtype in self.supertypes)

class TypedCompletor(object):
	def __init__(self):
		self.complete_with_types = Mock(return_value = [])

class TypeHoleInfoExtractor(object):
	def __init__(self):
		self.type_at_range = Mock(return_value = Fallible.fail(None))

class View(object):
	def __init__(self):
		self.text = 'test'

	def substr(self, range):
		return 'blah'

	def size(self):
		return 10

s = Fallible.succeed

class TypeMatchingCompletorSpec(unittest.TestCase):
	def setUp(self):
		self.view = View()
		self.commands = ExtraGhciCommands()
		self.completor = TypedCompletor()
		self.info_extractor = TypeHoleInfoExtractor()
		self.type_matching_completor = TypeMatchingCompletor(Sublime(), self.commands, self.completor, self.info_extractor, self.view)

	def test_when_there_are_no_completions_then_no_completions_are_produced(self):
		result = self.type_matching_completor.complete_with_types('', 4)
		self.assertEqual(result, [])

	def test_when_the_type_extractor_fails_the_same_completions_are_returned(self):
		completions = [('f', 'a'), ('g', 'b')]
		self.completor.complete_with_types.return_value = completions
		result = self.type_matching_completor.complete_with_types('', 4)
		self.assertEqual(result, completions)

	def _with_completions_and_type_expect(self, completions, type, output):
		self.completor.complete_with_types.return_value = completions
		self.info_extractor.type_at_range.return_value = Fallible.succeed(type)
		result = self.type_matching_completor.complete_with_types('', 4)
		self.assertEqual(result, output)

	def test_when_there_are_two_completions_and_the_first_is_equal_to_the_type_at_cursor_put_that_one_on_top(self):
		completions = [('f', s('a')), ('g', s('b'))]
		self._with_completions_and_type_expect(completions, 'a', completions)

	def test_when_there_are_two_completions_and_the_last_is_equal_to_the_type_at_cursor_put_that_one_on_top(self):
		self._with_completions_and_type_expect(
			[('f', s('a')), ('g', s('b'))],
			'b',
			[('g', s('b')), ('f', s('a'))])

	def test_when_there_are_three_completions_and_the_last_two_are_equal_to_the_type_at_cursor_put_those_two_on_top(self):
		self._with_completions_and_type_expect(
			[('f', s('a')), ('g', s('b')), ('h', s('b'))],
			'b',
			[('g', s('b')), ('h', s('b')), ('f', s('a'))])

	def test_when_there_are_two_completions_and_the_last_is_a_supertype_of_the_type_at_the_cursor_put_that_one_on_top(self):
		self.commands.supertypes = ['b']
		self._with_completions_and_type_expect(
			[('f', s('a')), ('g', s('b'))],
			't',
			[('g', s('b')), ('f', s('a'))])

	def test_when_there_are_three_completions_and_the_last_two_are_supertypes_of_the_type_at_the_cursor_put_those_two_on_top(self):
		self.commands.supertypes = ['b', 'c']
		self._with_completions_and_type_expect(
			[('f', s('a')), ('g', s('b')), ('h', s('c'))],
			't',
			[('g', s('b')), ('h', s('c')), ('f', s('a'))])
