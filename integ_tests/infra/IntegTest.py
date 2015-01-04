import SublimeGHCi.integ_tests.infra.IntegTestCommands as commands
from SublimeGHCi.integ_tests.infra.Results import Results
from SublimeGHCi.integ_tests.infra.CommandList import CommandList, copy_commands

class Context():
	def __init__(self, sublime, manager, window, results):
		self._sublime = sublime
		self._manager = manager
		self._window = window
		self._results = results

	def sublime(self):
		return self._sublime

	def manager(self):
		return self._manager

	def window(self):
		return self._window

	def results(self):
		return self._results

class IntegTest(object):
	def __init__(self):
		self._commands = CommandList()
		self._source_folders = []

	def add_command(self, command):
		self._commands.add_command(command)
		return self

	def using_source_folder(self, source_folder):
		self._source_folders.append(source_folder)
		return self

	def run(self, git_resetter, sublime, manager, window):
		# View to keep window open in case we close all other windows
		window.new_file()

		results = Results()
		context = Context(sublime, manager, window, results)
		self._commands.run(context)

		window.run_command('save_all')
		window.run_command('close_all')

		git_resetter.reset_folders_to_head(self._source_folders)

		return results.all_results()

copy_commands(IntegTest, commands)