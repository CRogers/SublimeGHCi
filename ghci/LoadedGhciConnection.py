from SublimeGHCi.common.Fallible import *

class LoadedGhciConnection(object):
	def __init__(self, connection):
		self._connection = connection

	def message(self, msg):
		if self._connection.loaded():
			return Fallible.succeed(self._connection.message(msg))
		else:
			return Fallible.fail('GHCi has not loaded')


	def loaded(self):
		return self._connection.loaded()

	def terminate(self):
		self._connection.terminate