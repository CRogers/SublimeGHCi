class TypeAddingCompletor(object):
	def __init__(self, completor, ghci_commands):
		self.completor = completor
		self.ghci_commands = ghci_commands

	def complete_with_types(self, prefix, location):
		completions = self.completor.complete(prefix, location)
		if len(completions) == 0:
			return []
		else:
			return [('yay', 'sometype')]