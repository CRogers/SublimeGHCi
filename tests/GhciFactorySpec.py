import unittest
from unittest.mock import *

from SublimeGHCi.ghci.GhciFactory import *

class GhciConnection(object):
	pass

class GhciConnectionFactory(object):
	def __init__(self):
		self.new_connection = Mock(return_value=GhciConnection())
		self.new_connection_for_view = Mock(return_value=GhciConnection())

class View(object):
	pass

class GhciFactorySpec(unittest.TestCase):
	def setUp(self):
		self.connection_factory = GhciConnectionFactory()
		self.ghci_factory = GhciFactory(self.connection_factory)

	def test_initialises_properly(self):
		pass