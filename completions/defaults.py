from SublimeGHCi.completions.Completor import *

def default_completor(ghci, view):
	return Completor(ghci, view)