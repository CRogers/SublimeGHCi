import unittest
import time

try:
	import integ_tests.utils
except ImportError:
	pass

try:
	import sublime
	import SublimeGHCi.SublimeGHCi
except ImportError:
	pass

def wait_until_loaded(view):
	while not SublimeGHCi.SublimeGHCi.manager.loaded(view).value():
		time.sleep(0.1)

def print_yay():
	view = sublime.active_window().active_view()
	wait_until_loaded(view)
	view.run_command('insert_text', {'point': 63, 'string':'a = f'})
	cs = SublimeGHCi.SublimeGHCi.manager.complete(view, 'f', 68)
	view.run_command('undo')
	view.window().run_command('close')
	return cs

class CompletionsIntegSpec(unittest.TestCase):
	def test_(self):
		cat = integ_tests.utils.run_integ_test(print_yay)
		self.assertEqual('[]', cat)