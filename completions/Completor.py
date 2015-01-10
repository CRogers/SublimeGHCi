class Completor(object):
    def __init__(self, commands):
        self._commands = commands

    def complete(self, prefix, location):
        return self._commands.completions(prefix).map_fail(lambda _:[]).value()

    def loaded(self):
        return self._commands.loaded()