import sublime

from SublimeGHCi.completions.CompletorFactory import *

def default_completor_factory(ghci_factory):
	return CompletorFactory(sublime, ghci_factory)