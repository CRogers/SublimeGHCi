import unittest
from unittest.mock import *

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.ghci.TypeHoleInfoExtractor import *

class GhciCommands(object):
	def __init__(self):
		self.load_haskell_file = Mock(return_value=Fallible.succeed('loaded'))
	
class TypeHoleInfoExtractorSpec(unittest.TestCase):
	def setUp(self):
		self.commands = GhciCommands()
		self.info_extractor = TypeHoleInfoExtractor(self.commands)

	def test_when_called_it_should_call_load_haskell_file_once(self):
		self.info_extractor.extract_info_from('foo ', 4)
		call_count = self.commands.load_haskell_file.call_count
		self.assertEqual(call_count, 1)

	#def test_when_called_it_should_call_load_haskell_file_and_supply_a_file_which_exists(self):
	#	self.info_extractor.extract_info_from('foo ', 4)
	#	self.commands.load_haskell_file.call_args