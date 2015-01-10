import unittest
from unittest.mock import *

from SublimeGHCi.common.EventHook import *
from SublimeGHCi.ghci.commands.GhciFactory import *


class Tempfile(object):
    pass

class GhciConnection(object):
    def __init__(self):
        self.on_loaded = Mock(return_value=EventHook())

class GhciConnectionFactory(object):
    def __init__(self):
        self.new_connection = Mock(return_value=GhciConnection())
        self.new_no_error_reporting_connection = Mock(return_value=GhciConnection())

class View(object):
    def __init__(self):
        self.file_name = Mock(return_value='Lol.hs')

class GhciFactorySpec(unittest.TestCase):
    def setUp(self):
        self.connection_factory = GhciConnectionFactory()
        self.ghci_factory = GhciFactory(Tempfile(), self.connection_factory)

    def test_initialises_properly(self):
        pass

    def test_can_create_a_ghci_for_view(self):
        self.ghci_factory.ghci_for_view(View())

    def test_can_create_a_new_type_hole_info_extractor(self):
        self.ghci_factory.new_type_hole_info_extractor(View())