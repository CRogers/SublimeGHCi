class TypeHoleInfoExtractor(object):
	def __init__(self, ghci_commands, type_hole_name = 'sublimeghci'):
		self._commands = ghci_commands
		self._type_hole_name = type_hole_name

	def extract_info_from(self, text, point):
		self._commands.load_from_string('_hole')