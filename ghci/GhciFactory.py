from SublimeGHCi.ghci.GhciConnection import *
from SublimeGHCi.ghci.AutoloadingGhciConnection import *
from SublimeGHCi.ghci.GhciCommands import *
from SublimeGHCi.ghci.ExtraGhciCommands import *
from SublimeGHCi.ghci.LoadedGhciCommands import *

class GhciFactory(object):
	def __init__(self, project_manager):
		self._project_manager = project_manager

	def new_ghci_for_view(self, view):
		project = self._project_manager.project_for_view(view)
		connection = AutoloadingGhciConnection(GhciConnection(project), view.file_name())
		return LoadedGhciCommands(ExtraGhciCommands(GhciCommands(connection)))