import sublime, uuid

class ErrorHighlights(object):
	def __init__(self, view):
		self.__view = view
		self.__key = str(uuid.uuid4())
		self.__add(regions)

	def __add(self, regions):
		flags = sublime.PERSISTENT | sublime.DRAW_NO_FILL
		self.__view.add_regions(self.__key, regions, 'keyword', 'dot', flags)

	def erase(self):
		self.__view.erase_regions(self.__key)