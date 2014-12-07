class CachingGhciFactory(object):
	def __init__(self, ghci_factory):
		self._ghci_factory = ghci_factory
		self._view_to_ghci = dict()

	def new_type_hole_info_extractor(self):
		return self._ghci_factory.new_type_hole_info_extractor()

	def ghci_for_view(self, view):
		key = view.buffer_id()
		if key not in self._view_to_ghci:
			self._view_to_ghci[key] = self._ghci_factory.ghci_for_view(view)
		return self._view_to_ghci[key]