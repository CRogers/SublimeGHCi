import unittest
from unittest.mock import *

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.completions.ModulePrefixCompletor import *

class GhciCommands(object):
	pass

class View(object):
	def __init__(self):
		self.text = 'test'

	def substr(self, point):
		if point < 0 or point > len(self.text):
			return '\x00'
		return self.text[point:(point+1)]
	
class ModulePrefixCompletorSpec(unittest.TestCase):
	def setUp(self):
		self.completor = GhciCommands()
		self.completor.complete = Mock(return_value=[])
		self.view = View()
		self.module_completor = ModulePrefixCompletor(self.completor, self.view)

	def _expect_prepend_to_succeed_with(self, view_text):
		self.view.text = view_text
		location = len(view_text)
		self.module_completor.complete('abc', location)
		self.completor.complete.assert_called_once_with(view_text, location)

	def test_when_the_preceeding_text_in_the_file_looks_like_a_single_module_prepend_the_module_to_the_prefix(self):
		self._expect_prepend_to_succeed_with('Module.abc')

	def test_when_the_preceeding_text_in_the_file_looks_like_a_double_module_prepend_both_modules_to_the_prefix(self):
		self._expect_prepend_to_succeed_with('Some.Module.abc')

	def test_when_the_preceeding_text_in_the_file_looks_like_a_triple_module_prepend_all_modules_to_the_prefix(self):
		self._expect_prepend_to_succeed_with('Hey.Some.Module.abc')

	def _expect_prepend_to_fail_with_abc(self, view_text):
		self.view.text = view_text
		location = len(view_text)
		self.module_completor.complete('abc', location)
		self.completor.complete.assert_called_once_with('abc', location)

	def test_when_the_preceeding_text_looks_like_a_module_but_has_no_dot_just_use_the_prefix(self):
		self._expect_prepend_to_fail_with_abc('Moduleabc')

	def test_when_the_preceeding_text_looks_like_a_module_but_on_a_previous_line_just_use_the_prefix(self):
		self._expect_prepend_to_fail_with_abc('Module.abc\n')

	def test_when_the_preceeding_text_starts_with_a_dot_but_then_no_capital_just_use_the_prefix(self):
		self._expect_prepend_to_fail_with_abc(' m.abc')

	def test_when_the_preceeding_text_starts_with_a_dot_but_the_beginning_of_the_file_is_reached_before_a_captial_just_use_the_prefix(self):
		self._expect_prepend_to_fail_with_abc('m.abc')

	def test_when_preceeding_text_is_just_a_dot_just_use_the_prefix(self):
		self._expect_prepend_to_fail_with_abc('.abc')