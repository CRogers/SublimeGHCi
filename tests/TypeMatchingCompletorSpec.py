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
f = Fallible.fail

def tick(str):
	return s(str + '\t\u2713')

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
		self._with_completions_and_type_expect(
			[('f', s('a')), ('g', s('b'))],
			'a',
			[('f', tick('a')), ('g', s('b'))])

	def test_when_there_are_two_completions_and_the_last_is_equal_to_the_type_at_cursor_put_that_one_on_top(self):
		self._with_completions_and_type_expect(
			[('f', s('a')), ('g', s('b'))],
			'b',
			[('g', tick('b')), ('f', s('a'))])

	def test_when_there_are_three_completions_and_the_last_two_are_equal_to_the_type_at_cursor_put_those_two_on_top(self):
		self._with_completions_and_type_expect(
			[('f', s('a')), ('g', s('b')), ('h', s('b'))],
			'b',
			[('g', tick('b')), ('h', tick('b')), ('f', s('a'))])

	def test_when_there_are_two_completions_and_the_last_is_a_supertype_of_the_type_at_the_cursor_put_that_one_on_top(self):
		self.commands.supertypes = ['b']
		self._with_completions_and_type_expect(
			[('f', s('a')), ('g', s('b'))],
			't',
			[('g', tick('b')), ('f', s('a'))])

	def test_when_there_are_three_completions_and_the_last_two_are_supertypes_of_the_type_at_the_cursor_put_those_two_on_top(self):
		self.commands.supertypes = ['b', 'c']
		self._with_completions_and_type_expect(
			[('f', s('a')), ('g', s('b')), ('h', s('c'))],
			't',
			[('g', tick('b')), ('h', tick('c')), ('f', s('a'))])

	def test_when_there_is_one_completion_with_a_failed_type_it_remains_failed(self):
		self.commands.supertypes = ['a']
		self._with_completions_and_type_expect(
			[('f', f('a'))],
			'a',
			[('f', f('a'))])

	def test_when_there_are_two_completions_with_one_failed_type_that_happens_to_be_a_super_type_it_shouldnt_go_on_top(self):
		self.commands.supertypes = ['a']
		self._with_completions_and_type_expect(
			[('g', s('b')), ('f', f('a'))],
			't',
			[('g', s('b')), ('f', f('a'))])