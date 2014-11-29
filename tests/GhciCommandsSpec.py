import unittest
from unittest.mock import *

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.ghci.GhciCommands import *

class GhciConnection(object):
	pass

class GhciCommandsSpec(unittest.TestCase):
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

	def test_when_the_type_command_returns_an_ambiguous_match_with_defined_at_and_imported_from_type_of_fails(self):
		self.connection.message.return_value = '''
<interactive>:1:1:
    Ambiguous occurrence ‘div’
    It could refer to either ‘Hstml.div’, defined at src/Hstml.hs:19:1
                          or ‘Prelude.div’,
                             imported from ‘Prelude’ (and originally defined in ‘GHC.Real’)'''

		type = self.commands.type_of('div')
		self.assertTrue(type.failed())
		self.assertEqual(type.value(), 'Ambiguous: Hstml.div or Prelude.div')

	def test_when_the_type_command_returns_an_ambiguous_match_with_import_from_twice_type_of_fails(self):
		self.connection.message.return_value = '''
<interactive>:1:1:
    Ambiguous occurrence ‘foldr’
    It could refer to either ‘Prelude.foldr’,
                             imported from ‘Prelude’ (and originally defined in ‘GHC.Base’)
                          or ‘Data.Foldable.foldr’, imported from ‘Data.Foldable’'''

		type = self.commands.type_of('foldr')
		self.assertTrue(type.failed())
		self.assertEqual(type.value(), 'Ambiguous: Prelude.foldr or Data.Foldable.foldr')

	def test_when_calling_kind_of_with_expression_should_send_appropriate_kind_of_command(self):
		self.commands.kind_of('A')
		self.connection.message.assert_called_once_with(':k (A)') 

	def test_when_the_kind_command_returns_a_kind_on_one_line_kind_of_returns_that_kind(self):
		self.connection.message.return_value = 'Functor :: (* -> *) -> Constraint'
		kind = self.commands.kind_of('Functor')
		self.assertTrue(kind.successful())
		self.assertEqual(kind.value(), '(* -> *) -> Constraint')

	def test_when_the_kind_command_returns_a_kind_on_two_lines_kind_of_returns_that_kind(self):
		self.connection.message.return_value = 'Foo\n ::\n    (k -> k)\n        -> *'
		kind = self.commands.kind_of('Foo')
		self.assertTrue(kind.successful())
		self.assertEqual(kind.value(), '(k -> k) -> *')

	def test_when_the_kind_command_returns_a_not_found_error_kind_of_fails(self):
		self.connection.message.return_value = '\n<interactive>:1:1: Not in scope: type constructor or class ‘Foo’'
		kind = self.commands.kind_of('Foo')
		self.assertTrue(kind.failed())

	def test_when_the_kind_command_returns_an_ambiguous_match_with_defined_at_and_imported_from_kind_of_fails(self):
		self.connection.message.return_value = '''
<interactive>:1:1:
    Ambiguous occurrence ‘Functor’
    It could refer to either ‘Hstml.Functor’,
                             defined at src/Hstml.hs:19:1
                          or ‘Prelude.Functor’,
                             imported from ‘Prelude’ (and originally defined in ‘GHC.Base’)'''

		kind = self.commands.kind_of('div')
		self.assertTrue(kind.failed())
		self.assertEqual(kind.value(), 'Ambiguous: Hstml.Functor or Prelude.Functor')

	def test_when_calling_load_haskell_file_with_a_filename_should_send_an_appropriate_load_command(self):
		self.commands.load_haskell_file('a/b.hs')
		self.connection.message.assert_called_once_with(':load "a/b.hs"')

	def test_when_the_load_command_fails_to_load_modules_load_haskell_file_should_fail(self):
		self.connection.message.return_value = '''
[1 of 2] Compiling Hstml            ( src/Hstml.hs, interpreted )’
Failed, modules loaded: Hstml.'''
		load = self.commands.load_haskell_file('a/b.hs')
		self.assertTrue(load.failed())

	def test_when_the_load_command_succeeds_to_load_modules_load_haskell_file_should_succeed(self):
		self.connection.message.return_value = '''
[1 of 1] Compiling Hstml            ( src/Hstml.hs, interpreted )
Ok, modules loaded: Hstml.'''
		load = self.commands.load_haskell_file('a/b.hs')
		self.assertTrue(load.successful())

	def test_when_an_expression_is_not_defined_run_expr_fails(self):
		self.connection.message.return_value = '\n<interactive>:114:1: Not in scope: ‘blah’'
		run = self.commands.run_expr('blah')
		self.assertTrue(run.failed())

	def test_when_an_expression_is_defined_run_expr_succeeds_with_the_result(self):
		self.connection.message.return_value = '2'
		run = self.commands.run_expr('1 + 1')
		self.assertTrue(run.successful())
		self.assertEqual(run.value(), '2')	

	def test_when_reload_is_called_it_performs_the_appropriate_command(self):
		self.commands.reload()
		self.connection.message.assert_called_once_with(':r')







