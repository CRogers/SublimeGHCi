import inspect

import SublimeGHCi.integ_tests.Commands as commands

class IntegTestContext():
	def __init__(self, manager, view):
		self.manager = manager
		self.view = view

class IntegTest(object):
	def __init__(self):
		self._commands = []

	def _add(self, command):
		self._commands.append(command)

	def run(self, context):
		result = None
		for command in self._commands:
			result = command.perform(context)

		for command in reversed(self._commands):
			command.undo(context)

		commands.Save().perform(context)
		window = context.view.window()
		window.run_command('close_window')

		return result

for name, cls in commands.__dict__.items():
	if not inspect.isclass(cls):
		continue
	def mkfunc(closure_class):
		def func(self, *args):
			self._add(closure_class(*args))
			return self
		return func
	setattr(IntegTest, cls.name, mkfunc(cls))