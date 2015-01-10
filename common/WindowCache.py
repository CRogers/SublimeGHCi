from SublimeGHCi.common.CreatingCache import *

class WindowCache(object):
    def __init__(self, creation_func):
        self._cache = CreatingCache(creation_func, lambda window: window.id())

    def get_for_window(self, window):
        return self._cache.get(window)