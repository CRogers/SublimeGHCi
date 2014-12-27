from SublimeGHCi.ghci.connection.LoadingGhciConnection import *
from SublimeGHCi.ghci.connection.FailedGhciConnection import *

class InternalGhciConnectionFactory(object):
	def __init__(self, subprocess, os, threading, project):
		self._subprocess = subprocess
		self._os = os
		self._threading = threading
		self._project = project

	def new_loading_ghci_connection(self):
		return LoadingGhciConnection(self, self._subprocess, self._os, self._threading, self._project)

	def new_failed_ghci_connection(self, failure_reason):
		return FailedGhciConnection(self, failure_reason)