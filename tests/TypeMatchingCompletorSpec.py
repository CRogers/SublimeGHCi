import unittest
from unittest.mock import *

from SublimeGHCi.completions.TypeMatchingCompletor import *

class TypedCompletor(object):
	def __init__(self):
		self.complete_with_types = Mock(return_value = [])

class ExtraGhciCommands(object):
	def __init__(self):
		pass

class View(object):
	def __init__(self):
		self.text = 'test'

class TypeMatchingCompletorSpec(unittest.TestCase):
	def setUp(self):
		self.view = View()
		self.completor = TypedCompletor()
		self.type_matching_completor = TypeMatchingCompletor(self.completor, self.view)

	def test_when_the_cursor_is_at_a_position_where_inserting_text_would_fail_compilation_no_completions_are_returned(self):
		self.view.text = 'import Prelude (map) '
		completions = self.type_matching_completor.complete('', len(self.view.text))
		self.assertEqual(completions, [])

	def test_when_there_are_no_completions_then_no_completions_are_produced(self):
		completions = self.type_matching_completor.complete('', 4)
		self.assertEqual(completions, [])

	def test_when_there_are_two_completions_but_one_of_them_fits_in_the_hole_at_cursor_put_that_one_on_top(self):
		pass