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
		self.commands = GhciCommands(self.connection)

	def test_when_close_is_called_terminate_is_called_on_connection(self):
		self.commands.close()
		self.connection.terminate.assert_called_once_with()