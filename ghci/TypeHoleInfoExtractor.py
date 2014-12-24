import re

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.common.Regexes import *

class TypeHoleInfoExtractor(object):
	def __init__(self, ghci_commands, type_hole_name = 'sublimeghci'):
		self._commands = ghci_commands
		self._type_hole = '_' + type_hole_name

	def _extract_hole_type(self, error_output):
		regex = r'Found hole ‘{}’\s*?with type: (.*?)\n\s*?(?:Relevant|Where)'.format(self._type_hole)
		match = re.search(regex, error_output, re.DOTALL)
		if match == None:
			return Fallible.fail(None)
		type_without_breaks = strip_whitespace_on_leading_lines(match.group(1))
		return Fallible.succeed(type_without_breaks)

	def _blah(self, text, start, length, holes):
		end = start + length
		new_text = text[:start] + holes + text[end:]
		return self._commands.load_from_string(new_text).value()

	def type_at_range(self, text, start, length):
		error_output = self._blah(text, start, length, self._type_hole)
		too_few = re.search(r'Probable cause: ‘.*?’ is applied to too few arguments', error_output)
		if too_few != None:
			error_output = self._blah(text, start, length, '{} _dummyhole'.format(self._type_hole))
		return self._extract_hole_type(error_output)