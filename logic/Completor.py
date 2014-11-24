class Completor(object):
	def __init__(self, commands, view):
		self._commands = commands
		self._view = view

	def complete(self, prefix, locations):
		return []