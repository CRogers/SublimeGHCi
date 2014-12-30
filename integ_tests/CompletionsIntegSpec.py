import unittest
import time

try:
	from integ_tests.utils import run_integ_test
except ImportError:
	pass

try:
	import sublime
	import SublimeGHCi.SublimeGHCi
	from SublimeGHCi.integ_tests.IntegTest import *
except ImportError:
	pass

def top_level_two_hole():
	view = sublime.active_window().active_view()
	manager = SublimeGHCi.SublimeGHCi.manager
	return (IntegTest()
		.wait()
		.append_text('a :: Foo\n')
		.append_text('a = takes ')
		.complete('Foo')
		.run(IntegTestContext(manager, view)))

def top_level_blah():
	view = sublime.active_window().active_view()
	manager = SublimeGHCi.SublimeGHCi.manager
	return (IntegTest()
		.wait()
		.append_text('a = takesFoo ')
		.complete('f')
		.run(IntegTestContext(manager, view)))

def top_level_completion_with(prefix):
	view = sublime.active_window().active_view()
	manager = SublimeGHCi.SublimeGHCi.manager
	return (IntegTest()
		.wait()
		.append_text('a = ')
		.complete(prefix)
		.run(IntegTestContext(manager, view)))

def add_3():
	view = sublime.active_window().active_view()
	manager = SublimeGHCi.SublimeGHCi.manager
	return (IntegTest()
		.wait()
		.append_text('3\n')
		.save()
		.append_text('a = ')
		.complete('Bar')
		.run(IntegTestContext(manager, view)))

def completion(expr, type):
	return ('{}\t{}'.format(expr, type), expr)

def with_tick(expr, type):
	fst, snd = completion(expr, type)
	return (fst + '\t\u2713', snd)

class CompletionsIntegSpec(unittest.TestCase):
	def test_no_completions(self):
		result = run_integ_test(['integ_tests/Completions/NoCompletions.hs'], top_level_completion_with, 'f')
		self.assertEqual(result, [])

	def test_one_completion(self):
		result = run_integ_test(['integ_tests/Completions/OneCompletion.hs'], top_level_completion_with, 'f')
		self.assertEqual(result, [with_tick('foo', 'Foo')])

	def test_should_suggest_only_module_prefixed_completions_after_dot(self):
		result = run_integ_test(['integ_tests/Completions/MultipleModules', 'integ_tests/Completions/MultipleModules/SecondModule.hs'], top_level_completion_with, 'F')
		self.assertEqual(result, [completion('FirstModule.bar','FirstModule.Bar')])

	def test_mutliple_modules(self):
		result = run_integ_test(['integ_tests/Completions/MultipleModules', 'integ_tests/Completions/MultipleModules/SecondModule.hs'], top_level_completion_with, 'b')
		self.assertEqual(result, [completion('bar', 'FirstModule.Bar')])

	def test_should_suggest_an_expression_which_fits_the_type_at_that_position_over_one_that_does_not(self):
		result = run_integ_test(['integ_tests/Completions/TypeHole.hs'], top_level_blah)
		self.assertEqual(result, [with_tick('fooForReal', 'Foo'), completion('fooFake','FooFake')])

	def test_should_put_a_tick_next_to_an_expression_when_it_fits_were_there_to_be_a_single_further_argument_to_the_function(self):
		result = run_integ_test(['integ_tests/Completions/TypeHole2.hs'], top_level_two_hole)
		self.assertEqual(result, [with_tick('Foo', 'Foo')])

	def test_should_put_a_tick_next_to_an_expression_when_it_fits_were_there_to_be_two_further_arguments_to_the_function(self):
		result = run_integ_test(['integ_tests/Completions/TypeHole3.hs'], top_level_two_hole)
		self.assertEqual(result, [with_tick('Foo', 'Foo')])

	def test_when_loading_a_cabal_library_with_compile_errors_completions_work_again_after_the_errors_have_been_fixed(self):
		result = run_integ_test(['integ_tests/Completions/DoesNotCompile', 'integ_tests/Completions/DoesNotCompile/DoesNotCompile.hs'], add_3)
		self.assertEqual(result, [with_tick('Bar', 'Bar')])