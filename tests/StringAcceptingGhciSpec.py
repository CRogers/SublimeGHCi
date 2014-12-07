import unittest
from unittest.mock import *

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.ghci.StringAcceptingGhci import *

class GhciCommands(object):
	def __init__(self):
		self.load_haskell_file = Mock(return_value=Fallible.succeed('loaded'))
	
class StringAcceptingGhciSpec(unittest.TestCase):
	def setUp(self):
		self.commands = GhciCommands()
		self.ghci = StringAcceptingGhci(self.commands, None, None)

	#def test_when_load_from_string_is_called(self):
	#	self.ghci.load_from_string('haskell file')