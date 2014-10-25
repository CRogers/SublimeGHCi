import subprocess
import re
import os
from threading import Thread

prompt_repeating_part = b']]]]]]]]]]]]]]]]'
prompt = (prompt_repeating_part + prompt_repeating_part[:-1]).decode('utf-8')

class GHCiConnection(object):
	def __init__(self, settings, on_loaded):
		self.__loaded = False
		self.__on_loaded = on_loaded
		self.__sp = self.__open(settings)
		t = Thread(target=self.__consume_beginning)
		t.daemon = True
		t.start()

	def __open(self, settings):
		project_directory = settings.project_directory()
		oldcwd = os.getcwd()
		if project_directory != None:
			os.chdir(project_directory)
		print("Creating ghic connection using {}".format(settings.ghci_command()))
		cat = subprocess.Popen(settings.ghci_command(), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
		if project_directory != None:
			os.chdir(oldcwd)
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
		return self.__read_until_prompt()

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
		self.__on_loaded()

	def loaded(self):
		return self.__loaded

	def terminate(self):
		self.__sp.terminate()