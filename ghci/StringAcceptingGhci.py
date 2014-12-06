class StringAcceptingGhci(object):
	def __init__(self, ghci_commands, os, tempfile):
		self._commands = ghci_commands