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

def wait_until_sublime_closes(popen):
	while not popen.poll():
		try:
			popen.wait(0.1)
			break
		except subprocess.TimeoutExpired:
			pass

def run_integ_test(func):
	env = os.environ.copy()
	env['INTEG_TESTS'] = '1'
	env['INTEG_NAME'] = func.__module__
	env['INTEG_FUNC'] = func.__name__
	env['INTEG_OUTPUT'] = os.path.abspath('integ_results')
	with open('integ_results', 'w+') as f:
		f.write('')
	p = subprocess.Popen([path, 'integ_tests/Completions/Completions1.hs'], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	wait_until_sublime_closes(p)
	with open('integ_results', 'r') as f:
		print(f.read())

class CompletionsIntegSpec(unittest.TestCase):
	def setUp(self):
		run_integ_test(print_yay)

	def test_(self):
		pass

	def test_2(self):
		pass