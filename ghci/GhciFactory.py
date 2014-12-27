from SublimeGHCi.ghci.ExtraGhciCommands import *
from SublimeGHCi.ghci.GhciCommands import *
from SublimeGHCi.ghci.HaskellFileAutoloader import *
from SublimeGHCi.ghci.StringAcceptingGhci import *
from SublimeGHCi.ghci.TypeHoleInfoExtractor import *

class GhciFactory(object):
	def __init__(self, tempfile, ghci_connection_factory):
		self._tempfile = tempfile
		self._connection_factory = ghci_connection_factory

	def _new_ghci(self, connection, file_name):
		commands = ExtraGhciCommands(GhciCommands(connection))
		HaskellFileAutoloader(commands, file_name)
		return commands

	def _new_string_accepting_ghci(self, connection, file_name):
		return StringAcceptingGhci(self._tempfile, self._new_ghci(connection, file_name))

	def new_type_hole_info_extractor(self, view):
		connection = self._connection_factory.new_connection(view)
		ghci_commands = self._new_string_accepting_ghci(connection, view.file_name())
		return TypeHoleInfoExtractor(ghci_commands)

	def ghci_for_view(self, view):
		connection = self._connection_factory.new_connection(view)
		return self._new_ghci(connection, view.file_name())