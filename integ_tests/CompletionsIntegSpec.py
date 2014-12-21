import unittest
import subprocess
import os, sys, os.path
try:
	import sublime
except ImportError:
	pass

path = '/Applications/Sublime Text.app/Contents/MacOS/Sublime Text'

def print_yay():
	return sublime.active_window().active_view().file_name()

class CompletionsIntegSpec(unittest.TestCase):
	def setUp(self):
		env = os.environ.copy()
		env['INTEG_TESTS'] = '1'
		env['INTEG_NAME'] = __name__
		env['INTEG_FUNC'] = 'print_yay'
		env['INTEG_OUTPUT'] = os.path.abspath('integ_results')
		with open('integ_results', 'w+') as f:
			f.write('')
		p = subprocess.Popen([path, 'integ_tests/Completions/Completions1.hs'], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		while not p.poll():
			try:
				p.wait(0.1)
				break
			except subprocess.TimeoutExpired:
				pass
		with open('integ_results', 'r') as f:
			print(f.read())

	def test_(self):
		pass

	def test_2(self):
		pass