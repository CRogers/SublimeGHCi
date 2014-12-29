from SublimeGHCi.controllers.Controller import *

class ControllerFactory(object):
	def __init__(self, project_manager, ghci_factory, completor_factory, error_reporter_factory):
		self._project_manager = project_manager
		self._error_reporter_factory = error_reporter_factory
		self._ghci_factory = ghci_factory
		self._completor_factory = completor_factory

	def controller_for_view(self, view):
		ghci = self._ghci_factory.ghci_for_view(view)
		completor = self._completor_factory.completor_for_view(view)
		project = self._project_manager.project_for_view(view)
		error_reporter = self._error_reporter_factory.error_reporter_for_view(view)
		return Controller(view, project, ghci, completor, error_reporter)