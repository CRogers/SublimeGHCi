class TypeMatchingCompletor(object):
	def __init__(self, sublime, completor, type_hole_info_extractor, view):
		self._sublime = sublime
		self._completor = completor
		self._info_extractor = type_hole_info_extractor
		self._view = view

	def _get_view_text(self):
		return self._view.substr(self._sublime.Region(0, self._view.size()))

	def _sort_completions_by_type(self, type, completions):
		matching = []
		non_matching = []
		for x, t in completions:
			if t == type:
				matching.append((x, t))
			else:
				non_matching.append((x, t))
		return matching + non_matching

	def complete_with_types(self, prefix, location):
		completions = self._completor.complete_with_types(prefix, location)
		text = self._get_view_text()
		return (self._info_extractor.type_at_point(text, location).switch(
			lambda type: self._sort_completions_by_type(type, completions),
			lambda _: completions))