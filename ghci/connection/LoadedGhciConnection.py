import re

from SublimeGHCi.common.EventHook import *
from SublimeGHCi.common.Fallible import *
from SublimeGHCi.ghci.connection.PromptIO import *

class LoadedGhciConnection(object):
	def __init__(self, sp):
		self.__sp = sp
		self._prompt = PromptIO(sp)
		self.next = EventHook()

	def message(self, msg):
		answer = self._prompt.message(msg)
		return Fallible.succeed(answer)

	def loaded(self):
		return True

	def terminate(self):
		self.__sp.terminate()