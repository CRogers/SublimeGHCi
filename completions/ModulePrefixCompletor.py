import itertools

class ModulePrefixCompletor(object):
	def __init__(self, completor, view):
		self._completor = completor
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
		prefix = self._scan_module(location - len(prefix) - 1) + prefix
		return self._completor.complete(prefix, location)

	def loaded(self):
		return self._completor.loaded()