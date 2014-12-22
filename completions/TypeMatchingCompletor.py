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
			if self._commands.is_supertype_of(type, t):
				matching.append((x, t))
			else:
				non_matching.append((x, t))
		print('m', matching, non_matching)
		return matching + non_matching

	def complete_with_types(self, prefix, location):
		print('yay')
		completions = self._completor.complete_with_types(prefix, location)
		print('no yay', completions)
		text = self._get_view_text()
		tap = self._info_extractor.type_at_point(text, location)
		print(tap)
		bah = (tap.switch(
			lambda type: self._sort_completions_by_type(type, completions),
			lambda _: completions))
		print('bah', bah)
		return bah

	def loaded(self):
		return self._commands.loaded() and self._completor.loaded()