from SublimeGHCi.completions.Completor import *
from SublimeGHCi.completions.ModulePrefixCompletor import *
from SublimeGHCi.completions.NoStringCompletor import *
from SublimeGHCi.completions.TypeAddingCompletor import *

def default_completor(ghci_commands, view):
	untyped_completor = NoStringCompletor(ModulePrefixCompletor(Completor(ghci_commands), view), view)
	return TypeAddingCompletor(untyped_completor, ghci_commands)