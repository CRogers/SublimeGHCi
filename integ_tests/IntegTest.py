import inspect

import SublimeGHCi.integ_tests.Commands as commands

class IntegTest(object):
	def __init__(self, manager, view):
		self._manager = manager
		self._view = view
		self._commands = []

	def _add(self, command):
		print(command)
		self._commands.append(command)

	def run(self):
		result = None
		for command in self._commands:
			ret = command.perform()
			if ret != None:
				result = ret

		for command in reversed(self._commands):
			command.undo()

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