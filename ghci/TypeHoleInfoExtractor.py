import re

from SublimeGHCi.common.Fallible import *

class TypeHoleInfoExtractor(object):
	def __init__(self, ghci_commands, type_hole_name = 'sublimeghci'):
		self._commands = ghci_commands
		self._type_hole = '_' + type_hole_name

	def _extract_hole_type(self, error_output):
		regex = r'Found hole ‘{}’ with type: (.*)'.format(self._type_hole)
		match = re.search(regex, error_output)
		if match == None:
			return Fallible.fail(None)
		return Fallible.succeed(match.group(1))

	def extract_info_from(self, text, point):
		new_text = text[:point] + self._type_hole + text[point:]
		error_output = self._commands.load_from_string(new_text).value()
		return self._extract_hole_type(error_output)