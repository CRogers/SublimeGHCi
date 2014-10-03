from SublimeGHCi.GHCiConnection import GHCiConnection
from SublimeGHCi.GHCiCommands import GHCiCommands
from SublimeGHCi.LoadedGHCiCommands import LoadedGHCiCommands

def new_ghci():
	return LoadedGHCiCommands(GHCiCommands(GHCiConnection()))

def key(view):
	return view.id()

class ViewGHCis(object):
	def __init__(self):
		self.__views = dict()

	def add(self, view):
		if key(view) in self.__views:
			return

		self.__views[key(view)] = new_ghci()

	def __remove(self, k):
		self.__views[k].connection().terminate()
		del self.__views[k]

	def remove(self, view):
		if key(view) not in self.__views:
			return

		self.__remove(key(view))

	def remove_all(self):
		for k in list(self.__views):
			self.__remove(k)

	def ghci_for(self, view):
		return self.__views[key(view)]