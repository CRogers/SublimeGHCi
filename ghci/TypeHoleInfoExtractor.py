class TypeHoleInfoExtractor(object):
	def __init__(self, ghci_commands, type_hole_name = 'sublimeghci'):
		self._commands = ghci_commands
		self._type_hole = '_' + type_hole_name

	def extract_info_from(self, text, point):
		new_text = text[:point] + self._type_hole + text[point:]
		self._commands.load_from_string(new_text)