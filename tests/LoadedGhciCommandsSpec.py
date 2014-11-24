import unittest
from unittest.mock import *

from SublimeGHCi.ghci.LoadedGhciCommands import *

class GhciCommands(object):
	pass

class LoadedGhciCommandsSpec(unittest.TestCase):
	def setUp(self):
		self.commands = GhciCommands()
		self.commands.loaded = Mock(return_value=False)
		self.loaded_commands = LoadedGhciCommands(self.commands)

	def test_when_inner_commands_loaded_returns_false_loaded_returns_false(self):
		self.assertFalse(self.loaded_commands.loaded())

	def test_when_inner_commands_loaded_returns_true_loaded_returns_true(self):
		self.commands.loaded.return_value = True
		self.assertTrue(self.loaded_commands.loaded())