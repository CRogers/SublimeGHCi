from SublimeGHCi.common.ViewCache import *

class CachingControllerFactory(object):
	def __init__(self, controller_factory):
		self._controller_cache = ViewCache(controller_factory.controller_for_view)

	def controller_for_view(self, view):
		return self._controller_cache.get_for_view(view)