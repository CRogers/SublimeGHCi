import tempfile
import subprocess
import os
import threading

from SublimeGHCi.ghci.commands.CachingGhciFactory import *
from SublimeGHCi.ghci.connection.GhciConnectionFactory import *
from SublimeGHCi.ghci.commands.GhciFactory import *


def default_ghci_factory(ghci_connection_factory):
	return CachingGhciFactory(GhciFactory(tempfile, ghci_connection_factory))

def default_ghci_connection_factory(project_manager, error_reporter):
	return GhciConnectionFactory(subprocess, os, threading, project_manager, error_reporter)