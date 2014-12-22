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

def top_level_f():
	return top_level_completion_with('f')

def top_level_F():
	return top_level_completion_with('F')

def top_level_b():
	return top_level_completion_with('b')

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

class CompletionsIntegSpec(unittest.TestCase):
	def test_no_completions(self):
		cat = run_integ_test(top_level_f, 'integ_tests/Completions/NoCompletions.hs')
		self.assertEqual(eval(cat), [])

	def test_one_completion(self):
		result = run_integ_test(top_level_f, 'integ_tests/Completions/OneCompletion.hs')
		self.assertEqual(eval(result), [('foo\tFoo', 'foo')])

	def test_should_suggest_only_module_prefixed_completions_after_dot(self):
		result = run_integ_test(top_level_F, 'integ_tests/Completions/MultipleModules', 'integ_tests/Completions/MultipleModules/SecondModule.hs')
		self.assertEqual(eval(result), [('FirstModule.bar\tFirstModule.Bar', 'FirstModule.bar')])

	def test_mutliple_modules(self):
		result = run_integ_test(top_level_b, 'integ_tests/Completions/MultipleModules', 'integ_tests/Completions/MultipleModules/SecondModule.hs')
		self.assertEqual(eval(result), [('bar\tFirstModule.Bar', 'bar')])

	def test_should_suggest_an_expression_which_fits_the_type_at_that_position_over_one_that_does_not(self):
		result = run_integ_test(top_level_blah, 'integ_tests/Completions/TypeHole.hs')
		self.assertEqual(eval(result), [('fooForReal\tFoo\t\u2713', 'fooForReal'), ('fooFake\tFooFake', 'fooFake')])