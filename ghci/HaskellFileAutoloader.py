from SublimeGHCi.ghci.GhciCommands import *

class HaskellFileAutoloader(object):
	def __init__(self, commands, file_name):
		self._commands = commands

	def _on_loaded(self):
		self._commands.load_haskell_file(self._file_name)