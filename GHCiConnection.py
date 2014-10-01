import subprocess
import re

prompt_repeating_part = b']]]]]]]]]]]]]]]]'
prompt = (prompt_repeating_part + prompt_repeating_part[:-1]).decode('utf-8')

class GHCiConnection(object):
	def __init__(self):
		self._sp = subprocess.Popen("/usr/local/bin/ghci", stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)

	def _read_until_prompt(self):
		data = b''
		while True:
			read = self._sp.stdout.read(len(prompt_repeating_part))
			if read == prompt_repeating_part:
				break
			data += read
		string = data.decode('utf-8')
		return re.sub(r'^\]*((.|\n)+)\n\]*$', r'\1', string)

	def message(self, msg):
		stdin = self._sp.stdin
		stdin.write(msg.encode('utf-8') + b'\n')
		stdin.flush()
		return self._read_until_prompt()

	def consume_beginning(self):
		print(self._sp.stdout.read1(1000000))
		print(self.message(':set prompt ' + prompt))