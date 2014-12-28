from threading import Semaphore
import random
from SublimeGHCi.common.EventHook import *
from SublimeGHCi.common.Fallible import *

class Box(object):
	def __init__(self, value):
		self.set(value)

	def get(self):
		return self._value

	def set(self, value):
		self._value = value

class FailedGhciConnection(object):
	def __init__(self, internal_ghci_factory, failure_reason):
		self._internal_ghci_factory = internal_ghci_factory
		self._failure_reason = failure_reason
		self.next = EventHook()

	def message(self, msg):
		return Fallible.fail('GHCi failed to load: \n\n' + self._failure_reason)

	def load_haskell_file(self, file_name):
		loading_ghci_connection = self._internal_ghci_factory.new_loading_ghci_connection()
		sema = Semaphore(value=0)
		after_loading_connection = Box(None)
		loading_ghci_connection.next.register(lambda next: [after_loading_connection.set(next), sema.release()])
		self.next.fire(loading_ghci_connection)
		sema.acquire()
		if after_loading_connection.get().failed():
			return self.message('')
		return after_loading_connection.get().load_haskell_file(file_name)

	def failed(self):
		return True

	def loaded(self):
		return False

	def terminate(self):
		pass