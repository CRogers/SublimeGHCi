import unittest
from unittest.mock import *

from SublimeGHCi.common.EventHook import *
from SublimeGHCi.ghci.AutoloadingGhciConnection import *

class GhciConnection(object):
	def __init__(self):
		self.on_loaded = EventHook()
		self.message = Mock(return_value='')
		self.loaded = Mock(return_value=True)
		self.terminate = Mock(return_value=None)

	def fire_loaded(self):
		self.on_loaded.fire()

class AutoloadingGhciConnectionSpec(unittest.TestCase):
	def setUp(self):
		self.connection = GhciConnection()
		self.file_name = 'Woop.hs'
		self.autoloading_connection = AutoloadingGhciConnection(self.connection, self.file_name)

	def test_when_connection_has_loaded_it_loads_given_file(self):
		self.connection.fire_loaded()
		self.connection.message.assert_called_once_with(':l Woop.hs')

	def test_when_connections_loaded_is_true_loaded_is_also_true(self):
		self.assertTrue(self.autoloading_connection.loaded())

	def test_when_connections_loaded_is_false_loaded_is_also_false(self):
		self.connection.loaded.return_value = False
		self.assertFalse(self.autoloading_connection.loaded())

	def test_when_terminate_is_called_connections_terminate_is_also_called(self):
		self.autoloading_connection.terminate()
		self.connection.terminate.asssert_called_once_with()