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
except ImportError:
	pass

def wait_until_loaded(view):
	while not SublimeGHCi.SublimeGHCi.manager.loaded(view):
		time.sleep(0.1)

def top_level_f():
	return top_level_completion_with('f')

def top_level_b():
	return top_level_completion_with('b')

def top_level_completion_with(prefix):
	view = sublime.active_window().active_view()
	wait_until_loaded(view)
	test = CompletionIntegTest(view, SublimeGHCi.SublimeGHCi.manager)
	test.append_text('a = ')
	cs = test.complete(prefix)
	test.undo()
	view.window().run_command('close')
	return cs

class CompletionsIntegSpec(unittest.TestCase):
	def test_(self):
		cat = integ_tests.utils.run_integ_test(top_level_f, 'integ_tests/Completions/NoCompletions.hs')
		self.assertEqual(eval(cat), [])

	def test_one_completion(self):
		result = integ_tests.utils.run_integ_test(top_level_f, 'integ_tests/Completions/OneCompletion.hs')
		self.assertEqual(eval(result), [('foo\tFoo', 'foo')])

	def test_mutliple_modules(self):
		result = integ_tests.utils.run_integ_test(top_level_b, 'integ_tests/Completions/MultipleModules', 'integ_tests/Completions/MultipleModules/SecondModule.hs')
		self.assertEqual(eval(result), [('bar\tFirstModule.Bar', 'bar')])