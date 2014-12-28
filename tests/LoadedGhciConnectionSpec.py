import unittest
from unittest.mock import *

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.ghci.connection.LoadedGhciConnection import *

class PromptIO(object):
	def __init__(self):
		self.message = Mock(return_value='answer')

class LoadedGhciConnectionSpec(unittest.TestCase):
	def setUp(self):
		self.prompt = PromptIO()
		self.connection = LoadedGhciConnection(self.prompt)

	def test_when_calling_load_haskell_file_with_a_filename_should_send_an_appropriate_load_command(self):
		self.connection.load_haskell_file('a/b.hs')
		self.prompt.message.assert_called_once_with(':load "a/b.hs"')

	def test_when_the_load_command_fails_to_load_modules_load_haskell_file_should_fail(self):
		self.prompt.message.return_value = '''
[1 of 2] Compiling Hstml            ( src/Hstml.hs, interpreted )’
Failed, modules loaded: Hstml.'''
		load = self.connection.load_haskell_file('a/b.hs')
		self.assertTrue(load.failed())

	def test_when_the_load_command_succeeds_to_load_modules_load_haskell_file_should_succeed(self):
		self.prompt.message.return_value = '''
[1 of 1] Compiling Hstml            ( src/Hstml.hs, interpreted )
Ok, modules loaded: Hstml.'''
		load = self.connection.load_haskell_file('a/b.hs')
		self.assertTrue(load.successful())