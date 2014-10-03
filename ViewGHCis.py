from SublimeGHCi.GHCiConnection import GHCiConnection
from SublimeGHCi.GHCiCommands import GHCiCommands
from SublimeGHCi.LoadedGHCiCommands import LoadedGHCiCommands

def new_ghci():
	return LoadedGHCiCommands(GHCiCommands(GHCiConnection()))

class ViewGHCis(object):
	def __init__(self):
		self.__views = dict()

	def add(self, view):
		if view.file_name() in self.__views:
			return

		self.__views[view.file_name()] = new_ghci()

	def __remove(self, file_name):
		self.__views[file_name].connection().terminate()
		del self.__views[file_name]

	def remove(self, view):
		if view.file_name() not in self.__views:
			return

		self.__remove(view.file_name())

	def remove_all(self):
		for file_name in list(self.__views):
			self.__remove(file_name)

	def ghci_for(self, view):
		return self.__views[view.file_name()]