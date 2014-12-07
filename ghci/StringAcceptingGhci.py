class StringAcceptingGhci(object):
	def __init__(self, tempfile, ghci_commands):
		self._tempfile = tempfile
		self._commands = ghci_commands

	def load_from_string(self, text):
		with self._tempfile.NamedTemporaryFile(suffix='.hs') as tf:
			tf.file.write(text.encode('utf-8'))
			return self._commands.load_haskell_file(tf.name)

	def is_supertype_of(self, subtype, supertype):
		return self._commands.is_supertype_of(subtype, supertype)