import re

from SublimeGHCi.common.EventHook import *
from SublimeGHCi.common.Fallible import *

prompt_repeating_part = b']]]]]]]]]]]]]]]]'

class LoadedGhciConnection(object):
	def __init__(self, sp):
		self.__sp = sp
		self.next = EventHook()

	def __read_until_prompt(self):
		data = b''
		while True:
			read = self.__sp.stdout.read(len(prompt_repeating_part))
			if read == prompt_repeating_part:
				break
			data += read
		string = data.decode('utf-8')
		return re.sub(r'^\]*((.|\n)+)\n\]*$', r'\1', string)

	def message(self, msg):
		stdin = self.__sp.stdin
		stdin.write(msg.encode('utf-8') + b'\n')
		stdin.flush()
		answer = self.__read_until_prompt()
		return Fallible.succeed(answer)

	def loaded(self):
		return True

	def terminate(self):
		self.__sp.terminate()