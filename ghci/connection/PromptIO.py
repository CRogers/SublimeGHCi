import re

prompt_repeating_part = b']]]]]]]]]]]]]]]]'
prompt = (prompt_repeating_part + prompt_repeating_part[:-1]).decode('utf-8')

class PromptIO(object):
	def __init__(self, file):
		self._file = file

	def set_prompt(self):
		self.message(':set prompt ' + prompt)

	def _read_until_prompt(self):
		data = b''
		while True:
			read = self._file.stdout.read(len(prompt_repeating_part))
			if read == prompt_repeating_part:
				break
			data += read
		string = data.decode('utf-8')
		return re.sub(r'^\]*((.|\n)+)\n\]*$', r'\1', string)

	def message(self, msg):
		stdin = self._file.stdin
		stdin.write(msg.encode('utf-8') + b'\n')
		stdin.flush()
		return self._read_until_prompt()