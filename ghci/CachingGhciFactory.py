class CachingGhciFactory(object):
	def __init__(self, ghci_factory):
		self._ghci_factory = ghci_factory

	def new_type_hole_info_extractor(self):
		return self._ghci_factory.new_type_hole_info_extractor()

	def new_ghci_for_view(self, view):
		return self._ghci_factory.new_ghci_for_view(view)