import unittest
from unittest.mock import *

from SublimeGHCi.completions.CompletorFactory import *

class Sublime(object):
    pass

class GhciCommands(object):
    pass

class TypeHoleInfoExtractor(object):
    pass

class GhciFactory(object):
    def ghci_for_view(self, view):
        return GhciCommands()

    def new_type_hole_info_extractor(self, view):
        return TypeHoleInfoExtractor()

class View(object):
    pass

class CompletorFactorySpec(unittest.TestCase):
    def setUp(self):
        self.completor_factory = CompletorFactory(Sublime(), GhciFactory())

    def test_initialises_properly(self):
        pass

    def test_can_make_completor_for_view(self):
        self.completor_factory.completor_for_view(View)