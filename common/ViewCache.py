class ViewCache(object):
	def __init__(self, creation_func):
		self._creation_func = creation_func

	def get_for_view(self, view):
		return self._creation_func(1)