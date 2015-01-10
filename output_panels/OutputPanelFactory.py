from SublimeGHCi.common.WindowCache import *
from SublimeGHCi.output_panels.OutputPanel import *

class OutputPanelFactory(object):
    def __init__(self):
        self._cache = WindowCache(OutputPanel)

    def output_panel_for_window(self, window):
        return self._cache.get_for_window(window)