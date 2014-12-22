from SublimeGHCi.common.Fallible import *

class LoadedGhciCommands(object):
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

	def __try_or_fail(self, funcName, *args):
		if self.loaded():
			return getattr(self.__commands, funcName)(*args)
		else:
			return Fallible.fail('GHCi has not yet loaded')

	def is_supertype_of(self, subtype, supertype):
		return self.__try_or_fail('is_supertype_of', subtype, supertype)

	def type_of(self, expr):
		return self.__try_or_fail('type_of', expr)

	def kind_of(self, expr):
		return self.__try_or_fail('kind_of', expr)

	def type_or_kind_of(self, expr):
		return self.__try_or_fail('type_or_kind_of', expr)

	def load_haskell_file(self, file_name):
		return self.__try_or_fail('load_haskell_file', file_name)

	def reload(self):
		return self.__try_or_fail('reload')

	def run_expr(self, expr):
		return self.__try_or_fail('run_expr', expr)