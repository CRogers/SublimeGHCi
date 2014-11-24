import unittest
from unittest.mock import *

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.ghci.GhciCommands import *

class GhciConnection(object):
	pass

class LoadedGhciCommandsSpec(unittest.TestCase):
	def setUp(self):
		self.connection = GhciConnection()
		self.connection.terminate = Mock()
		self.connection.loaded = Mock(return_value=True)
		self.commands = GhciCommands(self.connection)

	def test_when_close_is_called_terminate_is_called_on_connection(self):
		self.commands.close()
		self.connection.terminate.assert_called_once_with()

	def test_when_connection_loaded_returns_false_loaded_returns_false(self):
		self.connection.loaded.return_value = False
		self.assertFalse(self.commands.loaded())

	def test_when_connection_loaded_returns_true_loaded_returns_true(self):
		self.assertTrue(self.commands.loaded())