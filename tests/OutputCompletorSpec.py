import unittest
from unittest.mock import *

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