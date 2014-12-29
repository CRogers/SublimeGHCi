from SublimeGHCi.ghci.connection.InternalGhciConnectionFactory import *
from SublimeGHCi.ghci.connection.GhciConnection import *

class GhciConnectionFactory(object):
	def __init__(self, subprocess, os, threading, project_manager, error_reporter):
		self._subprocess = subprocess
		self._os = os
		self._threading = threading
		self._project_manager = project_manager
		self._error_reporter = error_reporter

	def new_connection(self, view):
		project = self._project_manager.project_for_view(view)
		internal_ghci_factory = InternalGhciConnectionFactory(self._subprocess, self._os, self._threading, project, self._error_reporter)
		return GhciConnection(internal_ghci_factory)