import inspect, time

import SublimeGHCi.integ_tests.Commands as commands

class IntegTest(object):
	def __init__(self, manager, view):
		self._manager = manager
		self._view = view
		self._commands = []

	def _add(self, command):
		self._commands.append(command)

	def run(self):
		self._view.settings().set('hot_exit', False)
		self._view.settings().set('remember_open_files', False)

		result = None
		for command in self._commands:
			result = command.perform()

		for command in reversed(self._commands):
			command.undo()

		commands.Save(self._manager, self._view).perform()
		time.sleep(1)
		window = self._view.window()
		window.run_command('close')
		time.sleep(1)
		window.run_command('close_window')
		time.sleep(1)
		
		return result

for name, cls in commands.__dict__.items():
	if not inspect.isclass(cls):
		continue
	def mkfunc(closure_class):
		def func(self, *args):
			self._add(closure_class(self._manager, self._view, *args))
			return self
		return func
	setattr(IntegTest, cls.name, mkfunc(cls))