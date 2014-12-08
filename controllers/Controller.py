class Controller(object):
	def __init__(self, project, ghci, completor, error_reporter):
		self._project = project
		self._error_reporter = error_reporter
		self._ghci = ghci
		self._completor = completor

	def _successfully_saved(self, blah):
		self._error_reporter.clear_errors()

	def loaded(self):
		return self._ghci.loaded()

	def saved(self):
		(self._ghci.reload()
			.map(self._successfully_saved)
			.map_fail(lambda err: self._error_reporter.report_errors(err, self._project.base_path())))

	def complete(self, prefix, location):
		return self._completor.complete(prefix, location)

	def close(self):
		self._ghci.close()