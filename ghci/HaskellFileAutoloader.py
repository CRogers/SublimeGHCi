from SublimeGHCi.ghci.GhciCommands import *

class HaskellFileAutoloader(object):
	def __init__(self, commands, file_name):
		self._commands = commands
		self._file_name = file_name

		commands.on_loaded().register(self._on_loaded)

	def _on_loaded(self):
		self._commands.load_haskell_file(self._file_name)