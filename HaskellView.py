from SublimeGHCi.GHCiConnection import GHCiConnection
from SublimeGHCi.GHCiCommands import GHCiCommands
from SublimeGHCi.LoadedGHCiCommands import LoadedGHCiCommands
from SublimeGHCi.Settings import Settings

class HaskellView(object):
	def __init__(self, view, error_reporter):
		self.__view = view
		self.__settings = Settings(view)
		self.__error_reporter = error_reporter
		self.__ghci = self.__new_ghci()

	def __new_ghci(self):
		return LoadedGHCiCommands(GHCiCommands(GHCiConnection(self.__settings, self.__compile)))

	def __compile(self):
		print('compiling {}'.format(self.__view.file_name()))
		return self.__ghci.load_haskell_file(self.__view.file_name())

	def saved(self):
		(self.__compile()
			.map(lambda _: self.__error_reporter.clear_errors())
			.mapFail(lambda err: self.__error_reporter.report_errors(err, self.__settings.project_directory())))

	def __autocomplete_entry(self, expr):
		return (expr + '\t' + self.__ghci.type_or_kind_of(expr).value(), expr)

	def completions(self, prefix):
		return (self.__ghci
			.completions(prefix)
			.map(lambda completions: [ self.__autocomplete_entry(x) for x in completions ]))

	def close(self):
		self.__ghci.connection().terminate()