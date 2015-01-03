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

class IntegTest(object):
	def __init__(self):
		self._commands = []

	def _add(self, command):
		self._commands.append(command)

	def with_file(self, with_view_test):
		return self

	def run(self):
		return []

for name, cls in commands.__dict__.items():
	if not inspect.isclass(cls):
		continue
	def mkfunc(closure_class):
		def func(self, *args):
			self._add(closure_class(*args))
			return self
		return func
	setattr(IntegTest, cls.name, mkfunc(cls))