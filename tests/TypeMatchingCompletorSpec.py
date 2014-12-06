import unittest
from unittest.mock import *

from SublimeGHCi.completions.TypeMatchingCompletor import *

class View(object):
	def __init__(self):
		self.text = 'test'

class TypeMatchingCompletorSpec(unittest.TestCase):
	def setUp(self):
		self.view = View()
		self.type_matching_completor = TypeMatchingCompletor()

	def test_when_the_cursor_is_at_a_position_where_inserting_text_would_fail_compilation_no_completions_are_returned(self):
		self.view.text = 'import Prelude (map) '
		completions = self.type_matching_completor.complete('', len(self.view.text))
		self.assertEqual(completions, [])
		pass