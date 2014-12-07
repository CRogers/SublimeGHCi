import unittest
from unittest.mock import *

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.ghci.TypeHoleInfoExtractor import *

class GhciCommands(object):
	def __init__(self):
		self.load_from_string = Mock(return_value=Fallible.succeed('loaded'))

type_hole_name = 'hole'
type_hole = '_' + type_hole_name

class TypeHoleInfoExtractorSpec(unittest.TestCase):
	def setUp(self):
		self.commands = GhciCommands()
		self.info_extractor = TypeHoleInfoExtractor(self.commands, type_hole_name)

	def test_when_called_calls_inner_commands_load_from_string_with_type_hole_in_given_location(self):
		self.info_extractor.extract_info_from('', 0)
		self.commands.load_from_string.assert_called_once_with(type_hole)