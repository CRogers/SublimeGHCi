class CachingControllerFactory(object):
	def setUp(self, controller_factory):
		self._controller_factory = controller_factory
		self._controller_cache = ViewCache(controller_factory.controller_for_view)

	def controller_for_view(self, view):
		self._controller_cache.get_for_view(view)