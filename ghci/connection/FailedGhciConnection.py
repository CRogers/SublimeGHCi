from SublimeGHCi.common.EventHook import *
from SublimeGHCi.common.Fallible import *

class FailedGhciConnection(object):
	def __init__(self, internal_ghci_factory, failure_reason):
		self._internal_ghci_factory = internal_ghci_factory
		self._failure_reason = failure_reason
		self.next = EventHook()

	def message(self, msg):
		loading_ghci_connection = self._internal_ghci_factory.new_loading_ghci_connection()
		self.next.fire(loading_ghci_connection)
		return loading_ghci_connection.message(msg)

	def loaded(self):
		return False

	def terminate(self):
		pass