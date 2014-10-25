from SublimeGHCi.Common import *

class LoadedGHCiCommands(object):
	def __init__(self, ghci_commands):
		self.__commands = ghci_commands

	def close(self):
		return self.__commands.close()

	def loaded(self):
		return self.__commands.loaded()

	def completions(self, prefix):
		if self.loaded():
			return self.__commands.completions(prefix)
		else:
			return Fallible.fail([])

	def __try_or_fail(self, funcName, arg):
		if self.loaded():
			return getattr(self.__commands, funcName)(arg)
		else:
			return Fallible.fail('GHCi has not yet loaded')

	def type_of(self, expr):
		return self.__try_or_fail('type_of', expr)

	def kind_of(self, expr):
		return self.__try_or_fail('kind_of', expr)

	def type_or_kind_of(self, expr):
		return self.__try_or_fail('type_or_kind_of', expr)

	def load_haskell_file(self, file_name):
		return self.__try_or_fail('load_haskell_file', file_name)