from SublimeGHCi.GHCiConnection import GHCiConnection
from SublimeGHCi.GHCiCommands import GHCiCommands
from SublimeGHCi.LoadedGHCiCommands import LoadedGHCiCommands

class TestRunner(object):
	def __init__(self, settings):
		self.__settings = settings
		self.__ghci = LoadedGHCiCommands(GHCiCommands(GHCiConnection(settings)))
		self.__ouput_panel = OutputPanel()

	def run_tests(self):
		self.__ghci.load_haskell_file(self.__settings.test_module())
		result = self.__ghci.run_expr(self.__settings.test_command())
		self.__ouput_panel.display_text(result)