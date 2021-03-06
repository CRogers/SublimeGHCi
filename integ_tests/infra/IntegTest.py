import SublimeGHCi.integ_tests.infra.IntegTestCommands as commands
from SublimeGHCi.integ_tests.infra.Results import Results
from SublimeGHCi.integ_tests.infra.CommandList import CommandList, copy_commands

class Context():
    def __init__(self, sublime, top, window, results):
        self._sublime = sublime
        self._top = top
        self._window = window
        self._results = results

    def sublime(self):
        return self._sublime

    def top(self):
        return self._top

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

    def run(self, sublime, top, window):
        # View to keep window open in case we close all other windows
        window.new_file()

        results = Results()
        context = Context(sublime, top, window, results)
        self._commands.run(context)

        window.run_command('save_all')
        window.run_command('close_all')

        return results.all_results()

copy_commands(IntegTest, commands)