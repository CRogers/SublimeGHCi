from SublimeGHCi.common.EventHook import *
from SublimeGHCi.common.Fallible import *

class FailedGhciConnection(object):
	def __init__(self, failure_reason):
		self._failure_reason = failure_reason
		self.next = EventHook()

	def message(self, msg):
		return Fallible.fail('Loading GHCi failed: ' + self._failure_reason)

	def loaded(self):
		return True

	def terminate(self):
		pass