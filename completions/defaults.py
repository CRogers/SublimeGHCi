from SublimeGHCi.completions.Completor import *
from SublimeGHCi.completions.ModulePrefixCompletor import *
from SublimeGHCi.completions.NoStringCompletor import *
from SublimeGHCi.completions.TypeAddingCompletor import *
from SublimeGHCi.completions.OutputCompletor import *

def default_completor(ghci_commands, view):
	untyped_completor = NoStringCompletor(ModulePrefixCompletor(Completor(ghci_commands), view), view)
	typed_completor = TypeAddingCompletor(untyped_completor, ghci_commands)
	return OutputCompletor(typed_completor)