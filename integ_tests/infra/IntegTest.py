import SublimeGHCi.integ_tests.infra.CommonCommands as common_commands
import SublimeGHCi.integ_tests.infra.Commands as commands
from SublimeGHCi.integ_tests.infra.CommandList import *
from SublimeGHCi.integ_tests.infra.Results import *

class WindowContext():
	def __init__(self, results, manager, window):
		self._results = results
		self._manager = manager
		self._window = window

	def manager(self):
		return self._manager

	def window(self):
		return self._window

	def results(self):
		return self._results


class IntegTest():
	def __init__(self):
		self._commands = CommandList()

	def add_command(self, command):
		self._commands.add_command(command)

	def run(self, manager, window):
		results = Results()
		context = WindowContext(results, manager, window)

		self._commands.perform(context)
		self._commands.undo(context)

		return results.all_results()


copy_commands(IntegTest, common_commands)
copy_commands(IntegTest, commands)