from SublimeGHCi.ghci.GhciCommands import *

class AutoloadingGhciConnection(object):
	def __init__(self, connection, file_name):
		self._connection = connection
		self._commands = GhciCommands(connection)
		self._file_name = file_name
		connection.on_loaded += self._on_loaded

	def _on_loaded(self):
		self._commands.load_haskell_file(self._file_name)

	def message(self, msg):
		return self._connection.message(msg)

	def loaded(self):
		return self._connection.loaded()

	def terminate(self):
		self._connection.terminate()