import re

from SublimeGHCi.common.EventHook import *

prompt_repeating_part = b']]]]]]]]]]]]]]]]'
prompt = (prompt_repeating_part + prompt_repeating_part[:-1]).decode('utf-8')

class GhciConnection(object):
	def __init__(self, subprocess, os, threading, project):
		self._subprocess = subprocess
		self._os = os
		self.__loaded = False
		self.on_loaded = EventHook()
		self.__sp = self.__open(project)
		t = threading.Thread(target=self.__consume_beginning)
		t.daemon = True
		t.start()

	def __open(self, project):
		oldcwd = self._os.getcwd()
		self._os.chdir(project.base_path())
		print("Creating ghci connection using {}".format(project.ghci_command()))
		cat = self._subprocess.Popen(project.ghci_command(),
			stdout=self._subprocess.PIPE,
			stdin=self._subprocess.PIPE,
			stderr=self._subprocess.STDOUT)
		self._os.chdir(oldcwd)
		return cat

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
		return answer

	def __consume_beginning(self):
		ghci_start = b'GHCi, version'
		full_message = b''
		last_n_chars = b''
		while last_n_chars != ghci_start:
			c = self.__sp.stdout.read(1)
			if len(c) == 0:
				print('Failed to load ghci: ' + full_message.decode('utf-8'))
				return
			full_message += c
			last_n_chars += c
			if len(last_n_chars) > len(ghci_start):
				last_n_chars = last_n_chars[1:]
		self.message(':set prompt ' + prompt)
		print('Loaded ghci')
		self.__loaded = True
		self.on_loaded.fire()

	def loaded(self):
		return self.__loaded

	def terminate(self):
		self.__sp.terminate()