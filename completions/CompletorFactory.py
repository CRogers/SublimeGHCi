from SublimeGHCi.completions.Completor import *
from SublimeGHCi.completions.ModulePrefixCompletor import *
from SublimeGHCi.completions.NoStringCompletor import *
from SublimeGHCi.completions.OutputCompletor import *
from SublimeGHCi.completions.TypeAddingCompletor import *
from SublimeGHCi.completions.TypeMatchingCompletor import *

class CompletorFactory(object):
    def __init__(self, sublime, ghci_factory):
        self._sublime = sublime
        self._ghci_factory = ghci_factory

    def _untyped_completor(self, ghci_commands, view):
        return NoStringCompletor(ModulePrefixCompletor(Completor(ghci_commands), view), view)

    def _typed_completor(self, ghci_commands, view):
        untyped_completor = self._untyped_completor(ghci_commands, view)
        typed_completor = TypeAddingCompletor(untyped_completor, ghci_commands)
        info_extractor = self._ghci_factory.new_type_hole_info_extractor(view)
        return TypeMatchingCompletor(self._sublime, ghci_commands, typed_completor, info_extractor, view)

    def completor_for_view(self, view):
        ghci_commands = self._ghci_factory.ghci_for_view(view)
        return OutputCompletor(self._typed_completor(ghci_commands, view))