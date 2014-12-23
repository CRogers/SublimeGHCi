class CompletionIntegTest(object):
	def __init__(self, view, manager):
		self._view = view
		self._manager = manager
		self._appends = 0

	def __enter__(self):
		return self

	def _get_end(self):
		return self._view.size()

	def append_text(self, string):
		end = self._get_end()
		self._view.run_command('insert_text', {'point': end, 'string': string})
		self._appends += 1

	def complete(self, string):
		self.append_text(string)
		print(string, self._get_end())
		return self._manager.complete(self._view, string, self._get_end())

	def __exit__(self, type, value, traceback):
		for x in range(0, self._appends):
			self._view.run_command('undo')