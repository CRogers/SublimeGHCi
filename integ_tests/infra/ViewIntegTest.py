import SublimeGHCi.integ_tests.infra.CommonCommands as common_commands
import SublimeGHCi.integ_tests.infra.ViewCommands as view_commands
from SublimeGHCi.integ_tests.infra.CommandList import *

class ViewContext():
    def __init__(self, window_context, view):
        self._window_context = window_context
        self._view = view

    def manager(self):
        return self._window_context.manager()

    def view(self):
        return self._view

    def window(self):
        return self._window_context.window()

    def results(self):
        return self._window_context.results()

class ViewIntegTest():
    def __init__(self, integ_test):
        self._commands = CommandList()
        self._integ_test = integ_test

    def add_command(self, command):
        self._commands.add_command(command)

    def perform(self, context):
        self._commands.perform(context)

    def undo(self, context):
        self._commands.undo(context)

    def back(self):
        return self._integ_test

    def run(self, manager, window):
        self._integ_test.run(manager, window)

copy_commands(ViewIntegTest, common_commands)
copy_commands(ViewIntegTest, view_commands)