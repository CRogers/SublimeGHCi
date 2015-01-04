from SublimeGHCi.integ_tests.infra.CommandList import CommandList

class AddResult():
    def perform(self, context):
        context.results().add_last_result()

class ViewContext():
    def __init__(self, window_context, view):
        self._window_context = window_context
        self._view = view

    def manager(self):
        return self._window_context.manager()

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

    def add_result(self):
        self.add_command(AddResult())
        return self

    def run(self, context):
        self._commands.run(context)

        return context.results().all_results()