import unittest
from unittest.mock import *

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.ghci.LoadedGhciConnection import *

class GhciConnection(object):
	def __init__(self):
		self.message = Mock(return_value='answer')
		self.loaded = Mock(return_value=False)

class LoadedGhciConnectionSpec(unittest.TestCase):
	def setUp(self):
		self.connection = GhciConnection()
		self.loaded_connection = LoadedGhciConnection(self.connection)

	def test_when_the_connection_has_not_loaded_message_fails(self):
		result = self.loaded_connection.message('blah')
		self.assertTrue(result.failed())

	def test_when_the_connection_is_loaded_the_result_from_the_inner_connections_message_is_pass_on_as_a_success(self):
		self.connection.loaded.return_value = True
		result = self.loaded_connection.message('blah')
		self.assertEqual(result, Fallible.succeed(self.connection.message.return_value))

	def test_when_the_connection_is_not_loaded_it_should_not_be_loaded_either(self):
		self.assertFalse(self.loaded_connection.loaded())

	def test_when_the_connection_is_loaded_it_should_be_loaded_too(self):
		self.connection.loaded.return_value = True
		self.assertTrue(self.loaded_connection.loaded())