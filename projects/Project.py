class Project(object):
	def __init__(self, ghci_command):
		self._ghci_command = ghci_command

	def ghci_command(self):
		return self._ghci_command