import unittest
from unittest.mock import *

from SublimeGHCi.completions.NoStringCompletor import *

class Completor():
	pass

class View():
	pass
	
class CompletorSpec(unittest.TestCase):
	def setUp(self):
		self.completor = Completor()
		self.completor.complete = Mock(return_value=['cat'])
		self.view = View()
		self.view.scope_name = Mock(return_value='scope')
		self.no_string_completor = NoStringCompletor(self.completor, self.view)

	def test_when_scope_does_not_contain_string_it_should_return_the_input(self):
		completions = self.no_string_completor.complete('c')
		self.assertEqual(completions, ['cat'])

	def test_when_scope_does_contain_string_it_should_return_no_results(self):
		self.view.scope_name.return_value = 'source.haskell string.quoted.double.haskell '
		completions = self.no_string_completor.complete('c')
		self.assertEqual(completions, ['cat'])