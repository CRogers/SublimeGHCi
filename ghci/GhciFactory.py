from SublimeGHCi.ghci.ExtraGhciCommands import *
from SublimeGHCi.ghci.GhciCommands import *
from SublimeGHCi.ghci.LoadedGhciCommands import *
from SublimeGHCi.ghci.StringAcceptingGhci import *
from SublimeGHCi.ghci.TypeHoleInfoExtractor import *

class GhciFactory(object):
	def __init__(self, tempfile, ghci_connection_factory):
		self._tempfile = tempfile
		self._connection_factory = ghci_connection_factory

	def _new_ghci(self, connection):
		return LoadedGhciCommands(ExtraGhciCommands(GhciCommands(connection)))

	def _new_string_accepting_ghci(self, connection):
		return StringAcceptingGhci(self._tempfile, self._new_ghci(connection))

	def new_type_hole_info_extractor(self, view):
		connection = self._connection_factory.new_connection(view)
		ghci_commands = self._new_string_accepting_ghci(connection)
		return TypeHoleInfoExtractor(ghci_commands)

	def ghci_for_view(self, view):
		connection = self._connection_factory.new_connection_for_view(view)
		return self._new_ghci(connection)