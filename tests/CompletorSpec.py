import unittest
from unittest.mock import *

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.logic.Completor import *

class GhciCommands(object):
	pass

class View(object):
	def __init__(self):
		self.text = ''

	def substr(self, point):
		return self.text[point:(point+1)]
	
class CompletorSpec(unittest.TestCase):
	def setUp(self):
		self.commands = GhciCommands()
		self.commands.completions = Mock(return_value=Fallible.succeed([]))
		self.view = View()
		self.completor = Completor(self.commands, self.view)

	def test_when_completions_returns_nothing_complete_returns_nothing(self):
		completed = self.completor.complete('abc', 123)
		self.assertEqual(completed, [])

	def test_when_completions_fails_complete_returns_nothing(self):
		self.commands.completions.return_value = Fallible.fail('failed')
		completed = self.completor.complete('abc', 123)
		self.assertEqual(completed, [])

	def test_when_completions_returns_a_value_complete_returns_it(self):
		self.commands.completions.return_value = Fallible.succeed(['abc'])
		completed = self.completor.complete('a', 123)
		self.assertEqual(completed, ['abc'])

	def test_when_the_preceeding_text_in_the_file_looks_like_a_module_prepend_the_module_to_the_prefix(self):
		self.view.text = 'Module.'
		self.completor.complete('abc', len(self.view.text))
		self.commands.completions.assert_called_once_with('Module.abc')