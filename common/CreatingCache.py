class CreatingCache(object):
	def __init__(self, creation_func, key_func):
		self._creation_func = creation_func
		self._key_func = key_func
		self._map = dict()

	def get(self, key_object):
		key = self._key_func(key_object)
		if key not in self._map:
			self._map[key] = self._creation_func(key_object)
		return self._map[key]