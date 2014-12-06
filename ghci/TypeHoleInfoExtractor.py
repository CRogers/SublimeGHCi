class TypeHoleInfoExtractor(object):
	def __init__(self, ghci_commands):
		self._commands = ghci_commands

	def extract_info_from(self, text, point):
		self._commands.load_haskell_file('lol')