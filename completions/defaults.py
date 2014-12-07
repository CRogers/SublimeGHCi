import sublime
import os, subprocess, threading

from SublimeGHCi.completions.CompletorFactory import *

def default_completor_factory(ghci_factory):
	return CompletorFactory(sublime, ghci_factory)