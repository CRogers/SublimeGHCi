import sublime, uuid, itertools

class ErrorHighlights(object):
    def __init__(self):
        self.__highlights = []

    def erase(self):
        for highlight in self.__highlights:
            highlight.erase()

    def highlight(self, error_positions):
        self.erase()
        for error_pos in error_positions:
            self.__highlights.append(ViewErrorHighlights(error_pos.view(), [error_pos.region()]))

class ViewErrorHighlights(object):
    def __init__(self, view, regions):
        self.__view = view
        self.__key = str(uuid.uuid4())
        self.__add(regions)

    def __add(self, regions):
        flags = sublime.DRAW_NO_FILL
        self.__view.add_regions(self.__key, regions, 'keyword', '', flags)

    def erase(self):
        self.__view.erase_regions(self.__key)