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
		pass

	def terminate(self):
		pass