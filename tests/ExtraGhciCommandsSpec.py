import unittest
from unittest.mock import *

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.ghci.ExtraGhciCommands import *

class GhciCommands(object):
	def __init__(self):
		self.type_of = Mock(return_value=Fallible.succeed('t'))
		self.kind_of = Mock(return_value=Fallible.succeed('k'))

class ExtraGhciCommandsSpec(unittest.TestCase):
	def setUp(self):
		self.commands = GhciCommands()
		self.extra_commands = ExtraGhciCommands(self.commands)

	def test_when_type_of_expression_succeeds_type_or_kind_of_returns_success_with_that_value(self):
		tok = self.extra_commands.type_or_kind_of('a')
		self.assertTrue(tok.successful())
		self.assertEqual(tok.value(), 't')

	def test_when_type_of_fails_but_kind_of_succeeds_type_or_kind_of_returns_success_with_kind_value(self):
		self.commands.type_of.return_value = Fallible.fail('')
		tok = self.extra_commands.type_or_kind_of('a')
		self.assertTrue(tok.successful())
		self.assertEqual(tok.value(), 'k')

	def test_when_type_of_and_kind_of_fail_type_or_kind_of_fails(self):
		self.commands.type_of.return_value = Fallible.fail('')
		self.commands.kind_of.return_value = Fallible.fail('')
		tok = self.extra_commands.type_or_kind_of('a')
		self.assertTrue(tok.failed())

	def test_when_is_supertype_of_is_called_it_calls_type_of_correctly(self):
		self.extra_commands.is_supertype_of('sub', 'sup')
		self.commands.type_of.assert_called_once_with('((let a = a in a) :: (sup)) :: (sub)')

	def test_when_type_of_returns_successfully_is_supertype_of_returns_true(self):
		is_supertype = self.extra_commands.is_supertype_of('sub', 'sup')
		self.assertTrue(is_supertype)

	def test_when_type_of_returns_unsuccessfully_is_supertype_of_returns_false(self):
		self.commands.type_of.return_value = Fallible.fail('failed')
		is_supertype = self.extra_commands.is_supertype_of('sub', 'sup')
		self.assertFalse(is_supertype)