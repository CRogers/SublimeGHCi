class AutoloadingGhciConnection(object):
	def __init__(self, connection, file_name):
		self._connection = connection
		self._file_name = file_name
		connection.on_loaded += self._on_loaded

	def _on_loaded(self):
		self._connection.message(':l "{}"'.format(self._file_name))

	def message(self, msg):
		return self._connection.message(msg)

	def loaded(self):
		return self._connection.loaded()

	def terminate(self):
		self._connection.terminate()