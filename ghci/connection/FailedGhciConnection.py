from SublimeGHCi.common.EventHook import *
from SublimeGHCi.common.Fallible import *

class FailedGhciConnection(object):
	def __init__(self, internal_ghci_factory, error_reporter, failure_reason):
		self._internal_ghci_factory = internal_ghci_factory
		self._failure_reason = failure_reason
		self.next = EventHook()

		error_reporter.report_errors(failure_reason)

	def message(self, msg):
		return Fallible.fail('GHCi failed to load')

	def load_haskell_file(self, file_name):
		loading_ghci_connection = self._internal_ghci_factory.new_loading_ghci_connection()
		self.next.fire(loading_ghci_connection)
		return Fallible.fail('Reloading ghci')

	def loaded(self):
		return False

	def terminate(self):
		pass