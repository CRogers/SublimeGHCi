import subprocess
import re

prompt_repeating_part = b']]]]]]]]]]]]]]]]'
prompt = (prompt_repeating_part + prompt_repeating_part[:-1]).decode('utf-8')

class GHCiConnection(object):
	def __init__(self):
		self.__sp = subprocess.Popen("/usr/local/bin/ghci", stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
		self.__loaded = False

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
		return self.__read_until_prompt()

	def consume_beginning(self):
		print(self.__sp.stdout.read1(1000000))
		print(self.message(':set prompt ' + prompt))
		self.__loaded = True

	def loaded(self):
		return self.__loaded

	def terminate(self):
		self.__sp.terminate()