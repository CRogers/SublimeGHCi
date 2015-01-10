class OutputCompletor(object):
    def __init__(self, typed_completor):
        self.typed_completor = typed_completor

    def complete(self, prefix, location):
        completions = self.typed_completor.complete_with_types(prefix, location)
        return [('{}\t{}'.format(expr, type.value()), expr) for expr, type in completions]

    def loaded(self):
        return self.typed_completor.loaded()