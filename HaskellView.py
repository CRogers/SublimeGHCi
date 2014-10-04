from SublimeGHCi.GHCiConnection import GHCiConnection
from SublimeGHCi.GHCiCommands import GHCiCommands
from SublimeGHCi.LoadedGHCiCommands import LoadedGHCiCommands

def new_ghci():
	return LoadedGHCiCommands(GHCiCommands(GHCiConnection()))

class HaskellView(object):
	def __init__(self, view, output_panel):
		self.__ghci = new_ghci()
		self.__view = view
		self.__output_panel = output_panel

	def saved(self):
		(self.__ghci
			.load_haskell_file(self.__view.file_name())
			.map(lambda _: self.__output_panel.hide())
			.mapFail(self.__output_panel.display_text))

	def __autocomplete_entry(self, expr):
		return (expr + '\t' + self.__ghci.type_or_kind_of(expr).value(), expr)

	def completions(self, prefix):
		return (self.__ghci
			.completions(prefix)
			.map(lambda completions: [ self.__autocomplete_entry(x) for x in completions ]))

	def close(self):
		self.__ghci.connection().terminate()