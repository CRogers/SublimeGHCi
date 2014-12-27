from SublimeGHCi.common.EventHook import *
from SublimeGHCi.common.Fallible import *
from SublimeGHCi.ghci.connection.LoadedGhciConnection import *
from SublimeGHCi.ghci.connection.FailedGhciConnection import *
from SublimeGHCi.ghci.connection.PromptIO import *

class LoadingGhciConnection(object):
	def __init__(self, subprocess, os, threading, project):
		self._subprocess = subprocess
		self._os = os

		self.next = EventHook()

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

	def __consume_beginning(self):
		ghci_start = b'GHCi, version'
		full_message = b''
		last_n_chars = b''
		while last_n_chars != ghci_start:
			c = self.__sp.stdout.read(1)
			if len(c) == 0:
				failure = full_message.decode('utf-8')
				self.next.fire(FailedGhciConnection(failure))
				return
			full_message += c
			last_n_chars += c
			if len(last_n_chars) > len(ghci_start):
				last_n_chars = last_n_chars[1:]
		PromptIO(self.__sp).set_prompt()
		print('Loaded ghci: ', full_message)
		self.next.fire(LoadedGhciConnection(self.__sp))

	def loaded(self):
		return False

	def message(self, msg):
		return Fallible.fail('GHCi is not yet loaded')

	def terminate(self):
		#TODO
		pass