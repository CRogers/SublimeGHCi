from SublimeGHCi.GHCiConnection import GHCiConnection
from SublimeGHCi.GHCiCommands import GHCiCommands
from SublimeGHCi.LoadedGHCiCommands import LoadedGHCiCommands

def new_ghci():
	return LoadedGHCiCommands(GHCiCommands(GHCiConnection()))

class HaskellView(object):
	def __init__(self, view, error_reporter):
		self.__ghci = new_ghci()
		self.__view = view
		self.__error_reporter = error_reporter

		print(self.__ghci.connection().loaded())
		self.__compile()

	def __compile(self):
		print('compiling {}'.format(self.__view.file_name()))
		return self.__ghci.load_haskell_file(self.__view.file_name())

	def saved(self):
		(self.__compile()
			.map(lambda _: self.__error_reporter.clear_errors())
			.mapFail(self.__error_reporter.report_errors))

	def __autocomplete_entry(self, expr):
		return (expr + '\t' + self.__ghci.type_or_kind_of(expr).value(), expr)

	def completions(self, prefix):
		return (self.__ghci
			.completions(prefix)
			.map(lambda completions: [ self.__autocomplete_entry(x) for x in completions ]))

	def close(self):
		self.__ghci.connection().terminate()