from SublimeGHCi.ghci.defaults import *
from SublimeGHCi.completions.defaults import *
from SublimeGHCi.Settings import Settings
from SublimeGHCi.TestRunner import TestRunner

class HaskellView(object):
	def __init__(self, view, error_reporter, test_highlights):
		self.__view = view
		self.__settings = Settings(view)
		self.__error_reporter = error_reporter
		self.__test_runner = TestRunner(self.__settings, view, test_highlights)
		self.__ghci = default_ghci_factory().new_ghci_for_view(view)
		self.__completor = default_completor(self.__ghci, self.__view)

	def __successfully_saved(self, blah):
		self.__error_reporter.clear_errors()
		self.__test_runner.run_tests()

	def saved(self):
		(self.__ghci.reload()
			.map(self.__successfully_saved)
			.map_fail(lambda err: self.__error_reporter.report_errors(err, self.__settings.project_directory())))

	def loaded(self):
		return self.__ghci.loaded()

	def complete(self, prefix, location):
		return self.__completor.complete(prefix, location)

	def close(self):
		self.__ghci.close()
		self.__test_runner.close()