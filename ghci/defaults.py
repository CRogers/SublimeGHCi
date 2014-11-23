from SublimeGHCi.ghci.GhciFactory import *
from SublimeGHCi.projects.defaults import *

def default_ghci_factory():
	return GhciFactory(default_project_manager())