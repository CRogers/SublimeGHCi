class OutputCompletor(object):
	def __init__(self, typed_completor):
		self.typed_completor = typed_completor

	def complete(self, prefix, location):
		return []