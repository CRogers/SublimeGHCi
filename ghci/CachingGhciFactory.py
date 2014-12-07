from SublimeGHCi.common.ViewCache import *

class CachingGhciFactory(object):
	def __init__(self, ghci_factory):
		self._ghci_factory = ghci_factory
		self._ghci_cache = ViewCache(self._ghci_factory.ghci_for_view)

	def new_type_hole_info_extractor(self):
		return self._ghci_factory.new_type_hole_info_extractor()

	def ghci_for_view(self, view):
		return self._ghci_cache.get_for_view(view)