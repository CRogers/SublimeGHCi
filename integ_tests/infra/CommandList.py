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