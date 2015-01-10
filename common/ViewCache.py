from SublimeGHCi.common.CreatingCache import *

class ViewCache(object):
    def __init__(self, creation_func):
        self._cache = CreatingCache(creation_func, lambda view: view.buffer_id())

    def get_for_view(self, view):
        return self._cache.get(view)