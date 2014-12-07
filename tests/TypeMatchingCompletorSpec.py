import unittest
from unittest.mock import *

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.completions.TypeMatchingCompletor import *

class TypedCompletor(object):
	def __init__(self):
		self.complete_with_types = Mock(return_value = [])

class TypeHoleInfoExtractor(object):
	def __init__(self):
		self.type_at_point = Mock(return_value = Fallible.fail(None))

class View(object):
	def __init__(self):
		self.text = 'test'

class TypeMatchingCompletorSpec(unittest.TestCase):
	def setUp(self):
		self.view = View()
		self.completor = TypedCompletor()
		self.info_extractor = TypedCompletor()
		self.type_matching_completor = TypeMatchingCompletor(self.completor, self.info_extractor, self.view)

	def test_when_there_are_no_completions_then_no_completions_are_produced(self):
		result = self.type_matching_completor.complete_with_types('', 4)
		self.assertEqual(result, [])

	def test_when_the_type_extractor_fails_the_same_completions_are_returned(self):
		completions = ['a', 'b']
		self.completor.complete_with_types.return_value = completions
		result = self.type_matching_completor.complete_with_types('', 4)
		self.assertEqual(result, completions)

	#def test_when_there_are_two_completions_but_one_of_them_fits_in_the_hole_at_cursor_put_that_one_on_top(self):
	#	pass