class TypeMatchingCompletor(object):
	def __init__(self, completor, view):
		self._completor = completor
		self._view = view

	def complete(self, prefix, location):
		return []