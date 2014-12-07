from SublimeGHCi.ghci.AutoloadingGhciConnection import *
from SublimeGHCi.ghci.GhciConnection import *

class GhciConnectionFactory(object):
	def __init__(self, subprocess, os, threading, project_manager):
		self._subprocess = subprocess
		self._os = os
		self._threading = threading
		self._project_manager = project_manager

	def new_connection(self):
		return GhciConnection(self._subprocess, self._os, self._threading, self._project_manager)

	def new_connection_for_view(self, view):
		return AutoloadingGhciConnection(self.new_connection(), view.file_name())