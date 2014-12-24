from SublimeGHCi.common.Fallible import *

class TypeMatchingCompletor(object):
	def __init__(self, sublime, commands, completor, type_hole_info_extractor, view):
		self._sublime = sublime
		self._commands = commands
		self._completor = completor
		self._info_extractor = type_hole_info_extractor
		self._view = view

	def _get_view_text(self):
		return self._view.substr(self._sublime.Region(0, self._view.size()))

	def _sort_completions_by_type(self, type, completions):
		matching = []
		non_matching = []
		for x, t in completions:
			if t.successful() and self._commands.is_supertype_of(t.value(), type):
				matching.append((x, Fallible.succeed(t.value() + '\t\u2713')))
			else:
				non_matching.append((x, t))
		return matching + non_matching

	def complete_with_types(self, prefix, location):
		completions = self._completor.complete_with_types(prefix, location)
		text = self._get_view_text()
		start = location - len(prefix)
		tap = self._info_extractor.type_at_range(text, start, len(prefix))
		return (tap.switch(
			lambda type: self._sort_completions_by_type(type, completions),
			lambda _: completions))

	def loaded(self):
		return self._commands.loaded() and self._completor.loaded() and self._info_extractor.loaded()