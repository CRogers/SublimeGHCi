from SublimeGHCi.ghci.AutoloadingGhciConnection import *
from SublimeGHCi.ghci.ExtraGhciCommands import *
from SublimeGHCi.ghci.GhciCommands import *
from SublimeGHCi.ghci.GhciConnection import *
from SublimeGHCi.ghci.LoadedGhciCommands import *
from SublimeGHCi.ghci.StringAcceptingGhci import *
from SublimeGHCi.ghci.TypeHoleInfoExtractor import *

class GhciFactory(object):
	def __init__(self, project_manager):
		self._project_manager = project_manager

	def _new_default_connection(self, connection):
		project = self._project_manager.project_for_view(view)
		return GhciConnection(project)

	def _new_ghci(self, connection):
		return LoadedGhciCommands(ExtraGhciCommands(GhciCommands(connection)))

	def _new_string_accepting_ghci(self, connection):
		return StringAcceptingGhci(self._new_ghci(connection))

	def new_type_hole_info_extractor(self):
		ghci_commands = self._new_string_accepting_ghci(self._new_default_connection())
		return TypeHoleInfoExtractor(ghci_commands)

	def new_ghci_for_view(self, view):
		connection = AutoloadingGhciConnection(self._new_default_connection(), view.file_name())
		return self._new_ghci(connection)