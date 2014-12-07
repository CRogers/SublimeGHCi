import tempfile, subprocess, os, threading

from SublimeGHCi.ghci.GhciFactory import *

def default_ghci_factory(ghci_connection_factory):
	return GhciFactory(tempfile, ghci_connection_factory)

def default_ghci_connection_factory(project_manager):
	return GhciConnectionFactory(subprocess, os, threading, project_manager)