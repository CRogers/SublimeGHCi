from SublimeGHCi.common.EventHook import *
from SublimeGHCi.common.Fallible import *

class FailedGhciConnection(object):
	def __init__(self, internal_ghci_factory, failure_reason):
		self._internal_ghci_factory = internal_ghci_factory
		self._failure_reason = failure_reason
		self.next = EventHook()

	def message(self, msg):
		self.next.fire(self._internal_ghci_factory.new_loading_ghci_connection())
		return Fallible.fail('Loading GHCi failed: ' + self._failure_reason)

	def loaded(self):
		return True

	def terminate(self):
		pass