import unittest
from unittest.mock import *

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.ghci.GhciCommands import *

class GhciConnection(object):
	pass

class LoadedGhciCommandsSpec(unittest.TestCase):
	def setUp(self):
		self.connection = GhciConnection()
		self.connection.terminate = Mock()
		self.connection.loaded = Mock(return_value=True)
		self.connection.message = Mock(return_value='')
		self.commands = GhciCommands(self.connection)

	def test_when_close_is_called_terminate_is_called_on_connection(self):
		self.commands.close()
		self.connection.terminate.assert_called_once_with()

	def test_when_connection_loaded_returns_false_loaded_returns_false(self):
		self.connection.loaded.return_value = False
		self.assertFalse(self.commands.loaded())

	def test_when_connection_loaded_returns_true_loaded_returns_true(self):
		self.assertTrue(self.commands.loaded())

	def test_when_calling_completions_with_prefix_should_send_appropriate_completions_command(self):
		self.commands.completions('a')
		self.connection.message.assert_called_once_with(':complete repl 1000000 "a"')

	def test_when_completions_have_no_results_should_return_no_results(self):
		self.connection.message.return_value = '0 0 ""'
		completions = self.commands.completions('a')
		self.assertTrue(completions.successful())
		self.assertEqual(completions.value(), [])

	def test_when_completions_has_two_results_should_return_a_successful_result_with_right_values(self):
		self.connection.message.return_value = '2 2 ""\n"abc"\n"abb"'
		completions = self.commands.completions('a')
		self.assertTrue(completions.successful())
		self.assertEqual(set(completions.value()), set(['abc', 'abb']))

	def test_when_calling_type_of_with_expression_should_send_appropriate_type_of_command(self):
		self.commands.type_of('a')
		self.connection.message.assert_called_once_with(':t (a)')

	def test_when_the_type_command_returns_a_type_on_one_line_type_of_returns_that_type(self):
		self.connection.message.return_value = 'undefined :: a'
		type = self.commands.type_of('undefined')
		self.assertTrue(type.successful())
		self.assertEqual(type.value(), 'a')

	def test_when_the_type_command_returns_a_type_on_two_lines_type_of_returns_that_type(self):
		self.connection.message.return_value = 'foo\n ::\n    (a -> b)\n        -> c'
		type = self.commands.type_of('foo')
		self.assertTrue(type.successful())
		self.assertEqual(type.value(), '(a -> b) -> c')

	def test_when_the_type_command_returns_a_not_found_error_type_of_fails(self):
		self.connection.message.return_value = '\n<interactive>:1:1: Not in scope: ‘cat’'
		type = self.commands.type_of('foo')
		self.assertTrue(type.failed())

	def test_when_the_type_command_returns_an_ambiguous_match_type_of_fails(self):
		self.connection.message.return_value = '''<interactive>:1:1:
    Ambiguous occurrence ‘div’
    It could refer to either ‘Hstml.div’, defined at src/Hstml.hs:19:1
                          or ‘Prelude.div’,
                             imported from ‘Prelude’ (and originally defined in ‘GHC.Real’)'''

		type = self.commands.type_of('div')
		self.assertTrue(type.failed())
		self.assertEqual(type.value(), 'Ambiguous: Hstml.div or Prelude.div')














