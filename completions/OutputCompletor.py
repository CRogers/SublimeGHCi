class OutputCompletor(object):
	def __init__(self, typed_completor):
		self.typed_completor = typed_completor

	def complete(self, prefix, location):
		completions = self.typed_completor.complete_with_types(prefix, location)
		if len(completions) == 0:
			return []
		else:
			return [('foo\tbar', 'foo')]