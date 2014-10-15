import sublime

class ExecutableProvider(object):
	def __init__(self, view):
		self.__settings = view.settings()

	def ghci_command(self):
		return self.__settings.get('ghci_command')