from SublimeGHCi.common.Fallible import *

class LoadedGhciConnection(object):
	def __init__(self, connection):
		self._connection = connection

	def message(self, msg):
		return Fallible.fail('GHCi not yet loaded')

	def loaded(self):
		pass

	def terminate(self):
		pass