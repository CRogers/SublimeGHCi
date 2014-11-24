import unittest
from unittest.mock import *

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.logic.Completor import *

class GhciCommands(object):
	pass

class View(object):
	pass

class CompletorSpec(unittest.TestCase):
	def setUp(self):
		self.commands = GhciCommands()
		self.commands.completions = Mock(return_value=Fallible.succeed([]))
		self.view = View()
		self.completor = Completor(self.commands, self.view)

	def test_when_completions_returns_nothing_complete_returns_nothing(self):
		completed = self.completor.complete('abc', [123])
		self.assertEqual(completed, [])