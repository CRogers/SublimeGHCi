import SublimeGHCi.integ_tests.infra.ViewIntegTestCommands as commands
from SublimeGHCi.integ_tests.infra.CommandList import CommandList, copy_commands

class ViewContext():
    def __init__(self, window_context, view):
        self._window_context = window_context
        self._view = view

    def sublime(self):
        return self._window_context.sublime()

    def top(self):
        return self._window_context.top()

    def window(self):
        return self._window_context.window()

    def results(self):
        return self._window_context.results()

    def view(self):
        return self._view

class ViewIntegTest():
    def __init__(self):
        self._commands = CommandList()

    def add_command(self, command):
        self._commands.add_command(command)
        return self

    def perform(self, context):
        self._commands.perform(context)

copy_commands(ViewIntegTest, commands)