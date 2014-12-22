class TypeAddingCompletor(object):
	def __init__(self, completor, ghci_commands):
		self.completor = completor
		self.ghci_commands = ghci_commands

	def complete_with_types(self, prefix, location):
		completions = self.completor.complete(prefix, location)
		return [(x, self.ghci_commands.type_or_kind_of(x)) for x in completions]

	def loaded(self):
		return self.completor.loaded()