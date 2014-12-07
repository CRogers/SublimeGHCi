class ViewCache(object):
	def __init__(self, creation_func):
		self._creation_func = creation_func
		self._view_map = dict()

	def get_for_view(self, view):
		key = view.buffer_id()
		if key not in self._view_map:
			self._view_map[key] = self._creation_func(view)
		return self._view_map[key]