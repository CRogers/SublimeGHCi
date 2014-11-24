import itertools

class Completor(object):
	def __init__(self, commands, view):
		self._commands = commands
		self._view = view

	def _scan_left(self, location):
		if self._view.substr(location) != '.':
			return ''
		total = '.'
		last_was_capital = False
		for i in range(location - 1, -1, -1):
			s = self._view.substr(i)
			if not s.isalpha():
				break
			last_was_capital = s.isupper()
			total = s + total

		if last_was_capital:
			return total
		else:
			return ''

	def _scan_module(self, location):
		i = location
		total = ''
		while i >= 0:
			out = self._scan_left(i)
			i -= len(out)
			total = out + total
			if out == '':
				return total

		return total

	def complete(self, prefix, location):
		prefix = self._scan_module(location - 1) + prefix
		return self._commands.completions(prefix).map_fail(lambda _:[]).value()