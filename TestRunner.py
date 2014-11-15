import re

from SublimeGHCi.Common import *
from SublimeGHCi.ErrorReporter import ErrorPos
from SublimeGHCi.Highlights import ErrorHighlights
from SublimeGHCi.GHCiConnection import GHCiConnection
from SublimeGHCi.GHCiCommands import GHCiCommands
from SublimeGHCi.LoadedGHCiCommands import LoadedGHCiCommands
from SublimeGHCi.OutputPanel import OutputPanel

def has_failed(result):
	failed = re.search(r'Exception: ExitFailure', result) != None
	return Fallible(failed, result)

def extract_error_positions(result):
	matches = re.finditer(r'\s*- (.*) FAILED', result)
	for match in matches:
		result = find_in_open_files(match.group(1))
		if result != None:
			yield ErrorPos(result["view"], result["region"])

class TestRunner(object):
	def __init__(self, settings):
		self.__settings = settings
		self.__ghci = LoadedGHCiCommands(GHCiCommands(GHCiConnection(settings)))
		self.__output_panel = OutputPanel()
		self.__highlights = ErrorHighlights()

	def __tests_failed(self, message):
		self.__output_panel.display_text(message)
		self.__highlights.highlight(extract_error_positions(message))

	def __tests_succeeded(self, message):
		self.__output_panel.hide()
		self.__highlights.erase()

	def run_tests(self):
		self.__ghci.load_haskell_file(self.__settings.test_module())
		(self.__ghci.run_expr(self.__settings.test_command())
			.bind(has_failed)
			.switch(self.__tests_failed, self.__tests_succeeded))

	def close(self):
		self.__ghci.close()