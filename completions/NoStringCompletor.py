class NoStringCompletor(object):
    def __init__(self, completor, view):
        self._completor = completor
        self._view = view

    def complete(self, prefix, location):
        if 'string' in self._view.scope_name(location):
            return []
        return self._completor.complete(prefix, location)

    def loaded(self):
        return self._completor.loaded()