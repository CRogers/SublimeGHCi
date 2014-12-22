import unittest
import time

try:
	import integ_tests.utils
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

def top_level_b():
	return top_level_completion_with('b')

def top_level_completion_with(prefix):
	view = sublime.active_window().active_view()
	manager = SublimeGHCi.SublimeGHCi.manager
	with GhciIntegTest(view, manager):
		with CompletionIntegTest(view, manager) as test:
			test.append_text('a = ')
			return test.complete(prefix)

class CompletionsIntegSpec(unittest.TestCase):
	def test_no_completions(self):
		cat = integ_tests.utils.run_integ_test(top_level_f, 'integ_tests/Completions/NoCompletions.hs')
		self.assertEqual(eval(cat), [])

	def test_one_completion(self):
		result = integ_tests.utils.run_integ_test(top_level_f, 'integ_tests/Completions/OneCompletion.hs')
		self.assertEqual(eval(result), [('foo\tFoo', 'foo')])

	def test_mutliple_modules(self):
		result = integ_tests.utils.run_integ_test(top_level_b, 'integ_tests/Completions/MultipleModules', 'integ_tests/Completions/MultipleModules/SecondModule.hs')
		self.assertEqual(eval(result), [('bar\tFirstModule.Bar', 'bar')])