import unittest
import time

try:
	from integ_tests.utils import run_integ_test
except ImportError:
	pass

try:
	import sublime
	import SublimeGHCi.SublimeGHCi
	from SublimeGHCi.integ_tests.CompletionIntegTest import *
	from SublimeGHCi.integ_tests.GhciIntegTest import *
except ImportError:
	pass

def top_level_two_hole():
	view = sublime.active_window().active_view()
	manager = SublimeGHCi.SublimeGHCi.manager
	with GhciIntegTest(view, manager):
		with CompletionIntegTest(view, manager) as test:
			test.append_text('a :: Foo\n')
			test.append_text('a = takes ')
			return test.complete('Foo')

def top_level_blah():
	view = sublime.active_window().active_view()
	manager = SublimeGHCi.SublimeGHCi.manager
	with GhciIntegTest(view, manager):
		with CompletionIntegTest(view, manager) as test:
			test.append_text('a = takesFoo ')
			return test.complete('f')

def top_level_completion_with(prefix):
	view = sublime.active_window().active_view()
	manager = SublimeGHCi.SublimeGHCi.manager
	with GhciIntegTest(view, manager):
		with CompletionIntegTest(view, manager) as test:
			test.append_text('a = ')
			return test.complete(prefix)

def add_3():
	view = sublime.active_window().active_view()
	manager = SublimeGHCi.SublimeGHCi.manager
	with GhciIntegTest(view, manager):
		with CompletionIntegTest(view, manager) as test:
			test.append_text('3\n')
			view.run_command('save')
			test.append_text('a = ')
			return test.complete('Bar')

class CompletionsIntegSpec(unittest.TestCase):
	def test_no_completions(self):
		cat = run_integ_test(['integ_tests/Completions/NoCompletions.hs'], top_level_completion_with, 'f')
		self.assertEqual(eval(cat), [])

	def test_one_completion(self):
		result = run_integ_test(['integ_tests/Completions/OneCompletion.hs'], top_level_completion_with, 'f')
		self.assertEqual(eval(result), [('foo\tFoo\t\u2713', 'foo')])

	def test_should_suggest_only_module_prefixed_completions_after_dot(self):
		result = run_integ_test(['integ_tests/Completions/MultipleModules', 'integ_tests/Completions/MultipleModules/SecondModule.hs'], top_level_completion_with, 'F')
		self.assertEqual(eval(result), [('FirstModule.bar\tFirstModule.Bar', 'FirstModule.bar')])

	def test_mutliple_modules(self):
		result = run_integ_test(['integ_tests/Completions/MultipleModules', 'integ_tests/Completions/MultipleModules/SecondModule.hs'], top_level_completion_with, 'b')
		self.assertEqual(eval(result), [('bar\tFirstModule.Bar', 'bar')])

	def test_should_suggest_an_expression_which_fits_the_type_at_that_position_over_one_that_does_not(self):
		result = run_integ_test(['integ_tests/Completions/TypeHole.hs'], top_level_blah)
		self.assertEqual(eval(result), [('fooForReal\tFoo\t\u2713', 'fooForReal'), ('fooFake\tFooFake', 'fooFake')])

	def test_should_put_a_tick_next_to_an_expression_when_it_fits_were_there_to_be_a_single_further_argument_to_the_function(self):
		result = run_integ_test(['integ_tests/Completions/TypeHole2.hs'], top_level_two_hole)
		self.assertEqual(eval(result), [('Foo\tFoo\t\u2713', 'Foo')])

	def test_should_put_a_tick_next_to_an_expression_when_it_fits_were_there_to_be_two_further_arguments_to_the_function(self):
		result = run_integ_test(['integ_tests/Completions/TypeHole3.hs'], top_level_two_hole)
		self.assertEqual(eval(result), [('Foo\tFoo\t\u2713', 'Foo')])

	@unittest.skip('feature not finished')
	def test_when_loading_a_cabal_library_with_compile_errors_completions_work_again_after_the_errors_have_been_fixed(self):
		result = run_integ_test(['integ_tests/Completions/DoesNotCompile', 'integ_tests/Completions/DoesNotCompile/DoesNotCompile.hs'], add_3)
		self.assertEqual(eval(result), [('Bar\tBar\t\u2713', 'Bar')])