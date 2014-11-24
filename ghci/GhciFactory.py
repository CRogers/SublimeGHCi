from SublimeGHCi.ghci.GhciConnection import *
from SublimeGHCi.ghci.GhciCommands import *
from SublimeGHCi.ghci.ExtraGhciCommands import *
from SublimeGHCi.ghci.LoadedGhciCommands import *

class GhciFactory(object):
	def __init__(self, project_manager):
		self._project_manager = project_manager

	def new_ghci_for_view(self, view, on_loaded=lambda: None):
		project = self._project_manager.project_for_view(view)
		connection = GhciConnection(project, on_loaded)
		return LoadedGhciCommands(ExtraGhciCommands(GhciCommands(connection)))