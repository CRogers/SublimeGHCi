import unittest
import subprocess
import os, sys

path = '/Applications/Sublime Text.app/Contents/MacOS/Sublime Text'

def print_yay():
	print('yay2')

class CompletionsIntegSpec(unittest.TestCase):
	def setUp(self):
		env = os.environ.copy()
		print(__name__)
		env['INTEG_TESTS'] = '1'
		env['INTEG_NAME'] = __name__
		env['INTEG_FUNC'] = 'print_yay'
		p = subprocess.Popen([path], env=env)

	def test_(self):
		pass
