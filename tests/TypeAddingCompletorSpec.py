import unittest
from unittest.mock import *

from SublimeGHCi.completions.TypeAddingCompletor import *

class TypeAddingCompletorSpec(unittest.TestCase):
	def setUp(self):
		self.type_adding_completor = TypeAddingCompletor()

	def test_when_underlying_completor_returns_no_results_return_no_results(self):
		completions = self.type_adding_completor.completion_with_types(self, 'abc', 3)
		self.assertEqual(completions, [])