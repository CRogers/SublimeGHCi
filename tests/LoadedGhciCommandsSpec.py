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
		self.commands.close = Mock()
		self.commands.completions = Mock(return_value=Fallible.succeed([]))
		self.commands.type_of = Mock(return_value=Fallible.succeed('type'))
		self.commands.kind_of = Mock(return_value=Fallible.succeed('kind'))
		self.commands.type_or_kind_of = Mock(return_value=Fallible.succeed('type or kind'))
		self.commands.reload = Mock(return_value=Fallible.succeed('response'))
		self.commands.run_expr = Mock(return_value=Fallible.succeed('run expr'))
		self.loaded_commands = LoadedGhciCommands(self.commands)

	def test_when_inner_commands_loaded_returns_false_loaded_returns_false(self):
		self.assertFalse(self.loaded_commands.loaded())

	def test_when_inner_commands_loaded_returns_true_loaded_returns_true(self):
		self.commands.loaded.return_value = True
		self.assertTrue(self.loaded_commands.loaded())

	def test_when_close_is_called_close_is_called_on_the_inner_commands(self):
		self.loaded_commands.close()
		self.commands.close.assert_called_once_with()

	def _when_commands_not_loaded_command_fails(self, command, *args):
		result = getattr(self.loaded_commands, command)(*args)
		self.assertTrue(result.failed())		

	def test_when_commands_not_loaded_completions_is_failed(self):
		self._when_commands_not_loaded_command_fails('completions', 'a')

	def test_when_commands_are_loaded_completions_is_successful_and_returns_the_inner_completions(self):
		self.commands.loaded.return_value = True
		self.commands.completions.return_value = Fallible.succeed(['ab'])
		completions = self.loaded_commands.completions('a')
		self.assertTrue(completions.successful())
		self.assertEqual(completions.value(), ['ab'])

	def test_when_commands_are_not_loaded_type_of_is_failed(self):
		self._when_commands_not_loaded_command_fails('type_of', 'a')

	def test_when_commands_are_loaded_type_of_is_successful_and_returns_the_inner_value(self):
		self.commands.loaded.return_value = True
		self.commands.type_of.return_value = Fallible.succeed('cat')
		completions = self.loaded_commands.type_of('a')
		self.assertTrue(completions.successful())
		self.assertEqual(completions.value(), 'cat')

	def test_when_commands_are_not_loaded_kind_of_is_failed(self):
		self._when_commands_not_loaded_command_fails('kind_of', 'a')

	def test_when_commands_are_loaded_kind_of_is_successful_and_returns_the_inner_value(self):
		self.commands.loaded.return_value = True
		self.commands.kind_of.return_value = Fallible.succeed('cat')
		completions = self.loaded_commands.kind_of('a')
		self.assertTrue(completions.successful())
		self.assertEqual(completions.value(), 'cat')

	def test_when_commands_are_not_loaded_type_or_kind_of_is_failed(self):
		self._when_commands_not_loaded_command_fails('type_or_kind_of', 'a')

	def test_when_commands_are_loaded_type_or_kind_of_is_successful_and_returns_the_inner_value(self):
		self.commands.loaded.return_value = True
		self.commands.type_or_kind_of.return_value = Fallible.succeed('cat')
		completions = self.loaded_commands.type_or_kind_of('a')
		self.assertTrue(completions.successful())
		self.assertEqual(completions.value(), 'cat')

	def test_when_commands_are_not_reload_file_is_failed(self):
		self._when_commands_not_loaded_command_fails('reload')

	def test_when_commands_are_loaded_reload_is_successful_and_returns_the_inner_value(self):
		self.commands.loaded.return_value = True
		self.commands.reload.return_value = Fallible.succeed('cat')
		completions = self.loaded_commands.reload()
		self.assertTrue(completions.successful())
		self.assertEqual(completions.value(), 'cat')

	def test_when_commands_are_not_loaded_run_expr_is_failed(self):
		self._when_commands_not_loaded_command_fails('run_expr', 'a')

	def test_when_commands_are_loaded_run_expr_is_successful_and_returns_the_inner_value(self):
		self.commands.loaded.return_value = True
		self.commands.run_expr.return_value = Fallible.succeed('cat')
		completions = self.loaded_commands.run_expr('a')
		self.assertTrue(completions.successful())
		self.assertEqual(completions.value(), 'cat')
