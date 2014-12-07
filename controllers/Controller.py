class Controller(object):
	def _init_(self, project_manager, ghci, completor, error_reporter):
		self._project_manager = project_manager
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
			.map_fail(lambda err: self._error_reporter.report_errors(err, self._settings.project_directory())))

	def complete(self, prefix, location):
		return self._completor.complete(prefix, location)

	def close(self):
		self._ghci.close()