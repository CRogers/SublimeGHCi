import unittest
from unittest.mock import *

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.ghci.TypeHoleInfoExtractor import *

class GhciCommands(object):
	def __init__(self):
		self.load_from_string = Mock(return_value=Fallible.succeed('loaded'))

class TypeHoleInfoExtractorSpec(unittest.TestCase):
	def setUp(self):
		self.commands = GhciCommands()
		self.info_extractor = TypeHoleInfoExtractor(self.commands, 'hole')

	def test_when_called_calls_inner_commands_load_from_string_with_type_hole_at_beginning(self):
		self.info_extractor.extract_info_from('', 0)
		self.commands.load_from_string.assert_called_once_with('_hole')

	def test_when_called_calls_inner_commands_load_from_string_with_type_hole_inside_text(self):
		self.info_extractor.extract_info_from('someFunc .  . anotherFunc', 11)
		self.commands.load_from_string.assert_called_once_with('someFunc . _hole . anotherFunc')