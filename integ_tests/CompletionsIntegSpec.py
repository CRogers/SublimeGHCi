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

def print_yay():
	view = sublime.active_window().active_view()
	wait_until_loaded(view)
	test = CompletionIntegTest(view, SublimeGHCi.SublimeGHCi.manager)
	test.append_text('a = ')
	cs = test.complete('f')
	test.undo()
	view.window().run_command('close')
	return cs

class CompletionsIntegSpec(unittest.TestCase):
	def test_(self):
		cat = integ_tests.utils.run_integ_test(print_yay)
		self.assertEqual('[]', cat)