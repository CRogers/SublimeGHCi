import inspect

import SublimeGHCi.integ_tests.Commands as commands

class Results():
	def __init__(self):
		self._results = []
		self._last_result = None

	def set_last_result(self, result):
		self._last_result = result

	def add_last_result(self):
		self._results.append(self._last_result)

	def all_results(self):
		return self._results

class AddResult():
	def perform(self, context):
		context.results().add_last_result()

class CommandList():
	def __init__(self):
		self._commands = []

	def add_command(self, command):
		self._commands.append(command)

	def run(self, context):
		for command in self._commands:
			result = command.perform(context)
			context.results().set_last_result(result)

		for command in reversed(self._commands):
			if hasattr(command, 'undo'):
				command.undo(context)

class ViewIntegTest():
	def __init__(self):
		self._commands = CommandList()

	def add_command(self, command):
		self._commands.add_command(command)
		return self

	def add_result(self):
		self.add_command(AddResult())
		return self

	def run(self, context):
		self._commands.run(context)

		return context.results().all_results()

class WithFile():
	def __init__(self, with_view_test):
		self._view_test = with_view_test(ViewIntegTest())

	def perform(self, context):
		self._view_test.run(context)

class Context():
	def __init__(self, manager, window, results):
		self._manager = manager
		self._window = window
		self._results = results

	def manager(self):
		return self._manager

	def window(self):
		return self._window

	def results(self):
		return self._results

class IntegTest(object):
	def __init__(self):
		self._commands = CommandList()

	def add_command(self, command):
		self._commands.add_command(command)
		return self

	def with_file(self, with_view_test):
		self.add_command(WithFile(with_view_test))
		return self

	def run(self, manager, window):
		results = Results()
		context = Context(manager, window, results)
		self._commands.run(context)

		return results.all_results()

for name, cls in commands.__dict__.items():
	if not inspect.isclass(cls):
		continue
	def mkfunc(closure_class):
		def func(self, *args):
			self._add(closure_class(*args))
			return self
		return func
	setattr(IntegTest, cls.name, mkfunc(cls))