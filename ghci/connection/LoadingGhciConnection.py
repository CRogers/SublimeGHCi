from SublimeGHCi.ghci.connection.FailedGhciConnection import *
from SublimeGHCi.ghci.connection.PromptIO import *

class LoadingGhciConnection(object):
    def __init__(self, internal_ghci_factory, subprocess, os, threading, project):
        self._internal_ghci_factory = internal_ghci_factory
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
            shell=True,
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
                self.next.fire(self._internal_ghci_factory.new_failed_ghci_connection(failure))
                return
            full_message += c
            last_n_chars += c
            if len(last_n_chars) > len(ghci_start):
                last_n_chars = last_n_chars[1:]
        PromptIO(self.__sp).set_prompt()
        print('Loaded ghci: ', full_message)
        self.next.fire(self._internal_ghci_factory.new_loaded_ghci_connection(PromptIO(self.__sp)))

    def loaded(self):
        return False

    def _not_yet_loaded(self):
        return Fallible.fail('GHCi is not yet loaded')

    def load_haskell_file(self, file_name):
        return self._not_yet_loaded()

    def message(self, msg):
        return self._not_yet_loaded()

    def terminate(self):
        #TODO
        pass