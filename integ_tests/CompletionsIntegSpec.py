import unittest
import subprocess
import os

path = '/Applications/Sublime Text.app/Contents/MacOS/Sublime Text'

class CompletionsIntegSpec(unittest.TestCase):
	def setUp(self):
		env = os.environ.copy()
		env['INTEG_TESTS'] = '1'
		p = subprocess.Popen([path], env=env)

	def test_(self):
		pass
