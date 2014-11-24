class Completor(object):
	def __init__(self, commands, view):
		self._commands = commands
		self._view = view

	def complete(self, prefix, location):
		if self._view.substr(location - 1) == '.':
			prefix = 'Module.' + prefix
		return self._commands.completions(prefix).map_fail(lambda _:[]).value()