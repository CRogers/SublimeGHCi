import unittest
from unittest.mock import *

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.ghci.LoadedGhciCommands import *

class GhciCommands(object):
	def __init__(self):
		self.loaded = Mock(return_value=False)
		self.close = Mock()
		self.completions = Mock(return_value=Fallible.succeed([]))
		self.type_of = Mock(return_value=Fallible.succeed('type'))
		self.kind_of = Mock(return_value=Fallible.succeed('kind'))
		self.type_or_kind_of = Mock(return_value=Fallible.succeed('type or kind'))
		self.load_haskell_file = Mock(return_value=Fallible.succeed('loaded'))
		self.reload = Mock(return_value=Fallible.succeed('response'))
		self.run_expr = Mock(return_value=Fallible.succeed('run expr'))

class LoadedGhciCommandsSpec(unittest.TestCase):
	def setUp(self):
		self.commands = GhciCommands()
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

	def _when_commands_are_loaded_command_is_successful_and_returns_inner_value(self, command, *args):
		self.commands.loaded.return_value = True
		getattr(self.commands, command).return_value = Fallible.succeed('result')
		result = getattr(self.loaded_commands, command)(*args)
		self.assertTrue(result.successful())
		self.assertEqual(result.value(), 'result')

	def test_when_commands_not_loaded_completions_is_failed(self):
		self._when_commands_not_loaded_command_fails('completions', 'a')

	def test_when_commands_are_loaded_completions_is_successful_and_returns_the_inner_completions(self):
		self._when_commands_are_loaded_command_is_successful_and_returns_inner_value('completions', 'a')

	def test_when_commands_are_not_loaded_type_of_is_failed(self):
		self._when_commands_not_loaded_command_fails('type_of', 'a')

	def test_when_commands_are_loaded_type_of_is_successful_and_returns_the_inner_value(self):
		self._when_commands_are_loaded_command_is_successful_and_returns_inner_value('type_of', 'a')

	def test_when_commands_are_not_loaded_kind_of_is_failed(self):
		self._when_commands_not_loaded_command_fails('kind_of', 'a')

	def test_when_commands_are_loaded_kind_of_is_successful_and_returns_the_inner_value(self):
		self._when_commands_are_loaded_command_is_successful_and_returns_inner_value('kind_of', 'a')

	def test_when_commands_are_not_loaded_type_or_kind_of_is_failed(self):
		self._when_commands_not_loaded_command_fails('type_or_kind_of', 'a')

	def test_when_commands_are_loaded_type_or_kind_of_is_successful_and_returns_the_inner_value(self):
		self._when_commands_are_loaded_command_is_successful_and_returns_inner_value('type_or_kind_of', 'a')

	def test_when_commands_are_not_reload_file_is_failed(self):
		self._when_commands_not_loaded_command_fails('reload')

	def test_when_commands_are_loaded_reload_is_successful_and_returns_the_inner_value(self):
		self._when_commands_are_loaded_command_is_successful_and_returns_inner_value('reload')

	def test_when_commands_are_not_loaded_run_expr_is_failed(self):
		self._when_commands_not_loaded_command_fails('run_expr', 'a')

	def test_when_commands_are_loaded_run_expr_is_successful_and_returns_the_inner_value(self):
		self._when_commands_are_loaded_command_is_successful_and_returns_inner_value('run_expr', 'a')

	def test_when_commands_are_not_loaded_load_haskell_file_is_failed(self):
		self._when_commands_not_loaded_command_fails('load_haskell_file', 'a')

	def test_when_commands_are_loaded_load_haskell_file_is_successful_and_returns_the_inner_value(self):
		self._when_commands_are_loaded_command_is_successful_and_returns_inner_value('load_haskell_file', 'a')