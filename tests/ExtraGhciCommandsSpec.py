import unittest
from unittest.mock import *

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.ghci.ExtraGhciCommands import *

class GhciCommands(object):
	pass

class LoadedGhciCommandsSpec(unittest.TestCase):
	def setUp(self):
		self.commands = GhciCommands()
		self.commands.type_of = Mock(return_value=Fallible.succeed('t'))
		self.commands.kind_of = Mock(return_value=Fallible.succeed('k'))
		self.extra_commands = ExtraGhciCommands(self.commands)

	def test_when_type_of_expression_succeeds_type_or_kind_of_returns_success_with_that_value(self):
		tok = self.extra_commands.type_or_kind_of('a')
		self.assertTrue(tok.successful())
		self.assertEqual(tok.value(), 't')