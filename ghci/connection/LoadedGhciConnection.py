import re

from SublimeGHCi.common.EventHook import *
from SublimeGHCi.common.Fallible import *
from SublimeGHCi.ghci.connection.PromptIO import *

def load_succeeded(response):
	return re.search(r'Failed, modules loaded:', response) == None

class LoadedGhciConnection(object):
	def __init__(self, prompt, view):
		self._prompt = prompt
		self.next = EventHook()

		self.load_haskell_file(view.file_name())

	def message(self, msg):
		answer = self._prompt.message(msg)
		return Fallible.succeed(answer)

	def load_haskell_file(self, file_name):
		msg = ':load "{}"'.format(file_name)
		return (self.message(msg)
			.bind(lambda response: Fallible.from_bool(load_succeeded, response)))

	def loaded(self):
		return True

	def terminate(self):
		self._prompt.terminate()