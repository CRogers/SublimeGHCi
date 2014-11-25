from SublimeGHCi.completions.Completor import *
from SublimeGHCi.completions.NoStringCompletor import *

def default_completor(ghci, view):
	return NoStringCompletor(Completor(ghci, view), view)