class Controller(object):
	def __init__(self, view, ghci, completor):
		self._view = view
		self._ghci = ghci
		self._completor = completor

	def loaded(self):
		return self._ghci.loaded() and self._completor.loaded()

	def saved(self):
		self._ghci.load_haskell_file(self._view.file_name())

	def complete(self, prefix, location):
		return self._completor.complete(prefix, location)

	def close(self):
		self._ghci.close()