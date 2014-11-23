class Project(object):
	def __init__(self, ghci_command, base_path):
		self._ghci_command = ghci_command
		self._base_path = base_path

	def ghci_command(self):
		return self._ghci_command

	def base_path(self):
		return self._base_path