class TypeMatchingCompletor(object):
	def __init__(self, completor, type_hole_info_extractor, view):
		self._completor = completor
		self._info_extractor = type_hole_info_extractor
		self._view = view

	def complete_with_types(self, prefix, location):
		return self._completor.complete_with_types(prefix, location)