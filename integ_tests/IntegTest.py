import inspect

import SublimeGHCi.integ_tests.Commands as commands

class IntegTestContext():
	def __init__(self, manager, view):
		self.manager = manager
		self.view = view
		self._last_result = None
		self._results = []

	def set_last_result(self, result):
		self._last_result = result

	def add_last_result(self):
		self._results.append(self._last_result)

	def all_results(self):
		return self._results

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
	def perform(self, results):
		results.add_last_result()

class CommandList():
	def __init__(self):
		self._commands = []

	def add_command(self, command):
		self._commands.append(command)

	def run(self, results):
		for command in self._commands:
			result = command.perform(results)
			results.set_last_result(result)

		for command in reversed(self._commands):
			if hasattr(command, 'undo'):
				command.undo(results)

class ViewIntegTest():
	def __init__(self):
		self._commands = CommandList()

	def add_command(self, command):
		self._commands.add_command(command)
		return self

	def add_result(self):
		self.add_command(AddResult())
		return self

	def run(self, results):
		self._commands.run(results)

		return results.all_results()

class WithFile():
	def __init__(self, with_view_test):
		self._view_test = with_view_test(ViewIntegTest())

	def perform(self, results):
		self._view_test.run(results)

class IntegTest(object):
	def __init__(self):
		self._commands = CommandList()

	def add_command(self, command):
		self._commands.add_command(command)
		return self

	def with_file(self, with_view_test):
		self.add_command(WithFile(with_view_test))
		return self

	def run(self):
		results = Results()
		self._commands.run(results)

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