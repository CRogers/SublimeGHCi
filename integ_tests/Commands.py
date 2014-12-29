import time

class AppendText(object):
	def __init__(self, view, string):
		self._view = view
		self._string

	def perform(self):
		end = self._view.size()
		self._view.run_command('insert_text', {'point': end, 'string': self._string})

	def undo(self):
		self._view.run_command('undo')

class Save(object):
	def __init__(self, view):
		self._view = view

	def perform(self):
		self._view.run_command('save')

class Wait(object):
	def __init__(self, manager, view):
		self._manager = manager
		self._view = view

	def perform(self):
		while not self._manager.loaded(self._view):
			time.sleep(0.1)

class Complete(object):
	def __init__(self, manager, view, string):
		self._manager = manager
		self._view = view
		self._string = string
		self._append = AppendText(view, string)

	def _complete(self):
		end = self._view.size()
		return self._manager.complete(self._view, string, end)

	def perform(self):
		self._append.perform()
		self._complete()
		Wait(self._manager, self._view).perform()
		return self._complete()

	def undo(self):
		self._append.undo()