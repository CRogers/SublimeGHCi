import re

from SublimeGHCi.Common import *
from SublimeGHCi.GHCiConnection import GHCiConnection
from SublimeGHCi.GHCiCommands import GHCiCommands
from SublimeGHCi.LoadedGHCiCommands import LoadedGHCiCommands

def new_ghci():
	return LoadedGHCiCommands(GHCiCommands(GHCiConnection()))

def key(view):
	return view.id()

def is_haskell_source_file(file_name):
	if file_name == None:
		return False
	
	return re.search(r'\.l?hs$', file_name) != None

class ViewGHCis(object):
	def __init__(self):
		self.__views = dict()

	def exists(self, view):
		return key(view) in self.__views

	def add(self, view):
		already_added = self.exists(view)
		if already_added or not is_haskell_source_file(view.file_name()):
			return

		print('creating new ghci for {}'.format(view.file_name()))
		ghci = new_ghci()
		self.__views[key(view)] = ghci
		ghci.load_haskell_file(view.file_name())

	def __remove(self, k):
		self.__views[k].connection().terminate()
		del self.__views[k]

	def remove(self, view):
		if not self.exists(view):
			return

		self.__remove(key(view))

	def remove_all(self):
		for k in list(self.__views):
			self.__remove(k)

	def ghci_for(self, view):
		if not self.exists(view):
			return Fallible.fail(None)
		else:
			return Fallible.succeed(self.__views[key(view)])
