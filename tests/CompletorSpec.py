import unittest
from unittest.mock import *

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.completions.Completor import *

class GhciCommands(object):
	pass

class View(object):
	def __init__(self):
		self.text = 'test'

	def substr(self, point):
		if point < 0 or point > len(self.text):
			return '\x00'
		return self.text[point:(point+1)]
	
class CompletorSpec(unittest.TestCase):
	def setUp(self):
		self.commands = GhciCommands()
		self.commands.completions = Mock(return_value=Fallible.succeed([]))
		self.view = View()
		self.completor = Completor(self.commands, self.view)

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

	def test_when_the_preceeding_text_in_the_file_looks_like_a_single_module_prepend_the_module_to_the_prefix(self):
		self.view.text = 'Module.abc'
		self.completor.complete('abc', len(self.view.text))
		self.commands.completions.assert_called_once_with('Module.abc')

	def test_when_the_preceeding_text_in_the_file_looks_like_a_double_module_prepend_both_modules_to_the_prefix(self):
		self.view.text = 'Some.Module.abc'
		self.completor.complete('abc', len(self.view.text))
		self.commands.completions.assert_called_once_with('Some.Module.abc')

	def test_when_the_preceeding_text_in_the_file_looks_like_a_triple_module_prepend_all_modules_to_the_prefix(self):
		self.view.text = 'Hey.Some.Module.abc'
		self.completor.complete('abc', len(self.view.text))
		self.commands.completions.assert_called_once_with('Hey.Some.Module.abc')

	def test_when_the_preceeding_text_looks_like_a_module_but_has_no_dot_just_use_the_prefix(self):
		self.view.text = 'Module'
		self.completor.complete('abc', len(self.view.text))
		self.commands.completions.assert_called_once_with('abc')

	def test_when_the_preceeding_text_looks_like_a_module_but_on_a_previous_line_just_use_the_prefix(self):
		self.view.text = 'Module.abc\n'
		self.completor.complete('abc', len(self.view.text))
		self.commands.completions.assert_called_once_with('abc')

	def test_when_the_preceeding_text_starts_with_a_dot_but_then_no_capital_just_use_the_prefix(self):
		self.view.text = ' m.abc'
		self.completor.complete('abc', len(self.view.text))
		self.commands.completions.assert_called_once_with('abc')

	def test_when_the_preceeding_text_starts_with_a_dot_but_the_beginning_of_the_file_is_reached_before_a_captial_just_use_the_prefix(self):
		self.view.text = 'm.abc'
		self.completor.complete('abc', len(self.view.text))
		self.commands.completions.assert_called_once_with('abc')

	def test_when_preceeding_text_is_just_a_dot_just_use_the_prefix(self):
		self.view.text = '.abc'
		self.completor.complete('abc', len(self.view.text))
		self.commands.completions.assert_called_once_with('abc')