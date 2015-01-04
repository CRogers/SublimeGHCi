import inspect

class CommandList():
    def __init__(self):
        self._commands = []

    def add_command(self, command):
        self._commands.append(command)

    def perform(self, context):
        for command in self._commands:
            result = command.perform(context)
            context.results().set_last_result(result)

    def undo(self, context):
        for command in reversed(self._commands):
            if hasattr(command, 'undo'):
                command.undo(context)

    def run(self, context):
        self.perform(context)
        self.undo(context)


def copy_commands(dest, module):
    for name, cls in module.__dict__.items():
        if not (inspect.isclass(cls) and hasattr(cls, 'name')):
            continue
        def mkfunc(closure_class):
            def func(self, *args):
                self.add_command(closure_class(*args))
                return self
            return func
        setattr(dest, cls.name, mkfunc(cls))