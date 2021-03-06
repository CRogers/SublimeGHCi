from SublimeGHCi.ghci.commands.ExtraGhciCommands import *
from SublimeGHCi.ghci.commands.GhciCommands import *
from SublimeGHCi.ghci.commands.StringAcceptingGhci import *
from SublimeGHCi.ghci.commands.TypeHoleInfoExtractor import *

class GhciFactory(object):
    def __init__(self, tempfile, ghci_connection_factory):
        self._tempfile = tempfile
        self._connection_factory = ghci_connection_factory

    def _new_ghci(self, connection, file_name):
        commands = ExtraGhciCommands(GhciCommands(connection))
        return commands

    def _new_string_accepting_ghci(self, connection, file_name):
        return StringAcceptingGhci(self._tempfile, self._new_ghci(connection, file_name))

    def new_type_hole_info_extractor(self, view):
        connection = self._connection_factory.new_no_error_reporting_connection(view)
        ghci_commands = self._new_string_accepting_ghci(connection, view.file_name())
        return TypeHoleInfoExtractor(ghci_commands)

    def ghci_for_view(self, view):
        connection = self._connection_factory.new_connection(view)
        return self._new_ghci(connection, view.file_name())