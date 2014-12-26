import unittest
from unittest.mock import *

from SublimeGHCi.ghci.LoadedGhciConnection import *

class GhciConnection(object):
	def __init__(self):
		self.message = Mock(return_value='blag')
		self.loaded = Mock(return_value=False)

class LoadedGhciConnectionSpec(unittest.TestCase):
	def setUp(self):
		self.connection = GhciConnection()
		self.loaded_connection = LoadedGhciConnection(self.connection)

	def test_when_the_connection_has_not_loaded_message_fails(self):
		result = self.loaded_connection.message('blah')
		self.assertTrue(result.failed())