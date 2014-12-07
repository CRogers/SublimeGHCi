class StringAcceptingGhci(object):
	def __init__(self, ghci_commands, tempfile):
		self._commands = ghci_commands
		self._tempfile = tempfile

	def load_from_string(self, text):
		with self._tempfile.NamedTemporaryFile(suffix='.hs') as tf:
			tf.file.write(text.encode('utf-8'))
			return self._commands.load_haskell_file(tf.name)