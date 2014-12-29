from SublimeGHCi.ghci.connection.InternalGhciConnectionFactory import *
from SublimeGHCi.ghci.connection.GhciConnection import *
from SublimeGHCi.error_reporters.NullErrorReporter import *

class GhciConnectionFactory(object):
	def __init__(self, subprocess, os, threading, project_manager, error_reporter):
		self._subprocess = subprocess
		self._os = os
		self._threading = threading
		self._project_manager = project_manager
		self._error_reporter = error_reporter

	def _new(self, view, error_reporter):
		project = self._project_manager.project_for_view(view)
		internal_ghci_factory = InternalGhciConnectionFactory(self._subprocess, self._os, self._threading, project, error_reporter)
		return GhciConnection(internal_ghci_factory)

	def new_connection(self, view):
		return self._new(view, self._error_reporter)

	def new_no_error_reporting_connection(self, view):
		return self._new(view, NullErrorReporter())