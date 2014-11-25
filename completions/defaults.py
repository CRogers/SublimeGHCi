from SublimeGHCi.completions.ModulePrefixCompletor import *
from SublimeGHCi.completions.NoStringCompletor import *

def default_completor(ghci, view):
	return NoStringCompletor(ModulePrefixCompletor(ghci, view), view)