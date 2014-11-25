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
		self.completor.complete = Mock(return_value=[])
		self.view = View()
		self.view.scope_name = Mock(return_value='scope')
		self.no_string_completor = NoStringCompletor(self.completor, self.view)

	def test_when_scope_does_not_contain_string_it_should_return_the_input(self):
		self.completor.complete.return_value = ['cat']
		completions = self.no_string_completor.complete('c')
		self.assertEqual(completions, ['cat'])
