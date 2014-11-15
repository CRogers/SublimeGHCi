import re

from SublimeGHCi.Common import *
from SublimeGHCi.GHCiConnection import GHCiConnection
from SublimeGHCi.GHCiCommands import GHCiCommands
from SublimeGHCi.LoadedGHCiCommands import LoadedGHCiCommands
from SublimeGHCi.OutputPanel import OutputPanel

def has_failed(result):
	failed = re.search(r'Exception: ExitFailure', result) != None
	return Fallible(failed, result)

class TestRunner(object):
	def __init__(self, settings):
		self.__settings = settings
		self.__ghci = LoadedGHCiCommands(GHCiCommands(GHCiConnection(settings)))
		self.__ouput_panel = OutputPanel()

	def run_tests(self):
		self.__ghci.load_haskell_file(self.__settings.test_module())
		(self.__ghci.run_expr(self.__settings.test_command())
			.bind(has_failed)
			.map(self.__ouput_panel.display_text))