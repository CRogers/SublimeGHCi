import unittest
from unittest.mock import *

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.ghci.LoadedGhciCommands import *

class GhciCommands(object):
	pass

class LoadedGhciCommandsSpec(unittest.TestCase):
	def setUp(self):
		self.commands = GhciCommands()
		self.commands.loaded = Mock(return_value=False)
		self.commands.completions = Mock(return_value=Fallible.succeed([]))
		self.commands.type_of = Mock(return_value=Fallible.succeed('type'))
		self.loaded_commands = LoadedGhciCommands(self.commands)

	def test_when_inner_commands_loaded_returns_false_loaded_returns_false(self):
		self.assertFalse(self.loaded_commands.loaded())

	def test_when_inner_commands_loaded_returns_true_loaded_returns_true(self):
		self.commands.loaded.return_value = True
		self.assertTrue(self.loaded_commands.loaded())

	def test_when_commands_not_loaded_completions_is_failed_and_empty(self):
		completions = self.loaded_commands.completions('a')
		self.assertTrue(completions.failed())
		self.assertEqual(completions.value(), [])

	def test_when_commands_are_loaded_completions_is_successful_and_returns_the_inner_completions(self):
		self.commands.loaded.return_value = True
		self.commands.completions.return_value = Fallible.succeed(['ab'])
		completions = self.loaded_commands.completions('a')
		self.assertTrue(completions.successful())
		self.assertEqual(completions.value(), ['ab'])

	def test_when_commands_are_not_loaded_type_of_is_failed(self):
		completions = self.loaded_commands.type_of('a')
		self.assertTrue(completions.failed())

	def test_when_commands_are_loaded_type_of_is_successful_and_returns_the_inner_value(self):
		self.commands.loaded.return_value = True
		self.commands.type_of.return_value = Fallible.succeed('cat')
		completions = self.loaded_commands.type_of('a')
		self.assertTrue(completions.successful())
		self.assertEqual(completions.value(), 'cat')