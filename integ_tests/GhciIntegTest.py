import time

class GhciIntegTest(object):
	def __init__(self, view, manager):
		print('------------- create')
		self._view = view
		self._manager = manager

	def __enter__(self):
		while not self._manager.loaded(self._view):
			time.sleep(0.1)

	def __exit__(self, type, value, traceback):
		print('------------- exit')
		self._view.window().run_command('close')