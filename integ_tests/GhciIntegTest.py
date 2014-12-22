import time

class GhciIntegTest(object):
	def __init__(self, view, manager):
		print('------------- create')
		self._view = view
		self._manager = manager
		while not self._manager.loaded(self._view).value():
			time.sleep(0.1)

	def __enter__(self):
		pass

	def __exit__(self, type, value, traceback):
		print('------------- exit')
		self._view.window().run_command('close')