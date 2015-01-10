from SublimeGHCi.controllers.Controller import *

class ControllerFactory(object):
    def __init__(self, ghci_factory, completor_factory):
        self._ghci_factory = ghci_factory
        self._completor_factory = completor_factory

    def controller_for_view(self, view):
        ghci = self._ghci_factory.ghci_for_view(view)
        completor = self._completor_factory.completor_for_view(view)
        return Controller(view, ghci, completor)