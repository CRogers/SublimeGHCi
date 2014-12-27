import unittest
from unittest.mock import *

from SublimeGHCi.common.EventHook import *
from SublimeGHCi.ghci.HaskellFileAutoloader import *

class GhciCommands(object):
	def __init__(self):
		self.on_loaded = Mock(return_value=EventHook())
		self.load_haskell_file = Mock(return_value=EventHook())

	def fire_loaded(self):
		self.on_loaded().fire()

class HaskellFileAutoloaderSpec(unittest.TestCase):
	def setUp(self):
		self.commands = GhciCommands()
		self.file_name = 'Woop.hs'
		self.autoloading_commands = HaskellFileAutoloader(self.commands, self.file_name)

	def test_when_commands_has_loaded_it_loads_given_file(self):
		self.commands.fire_loaded()
		self.commands.message.assert_called_once_with(self.file_name)