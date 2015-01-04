import sublime_plugin

from SublimeGHCi.integ_tests.infra.Common import save_integ_exceptions

from SublimeGHCi.error_reporters.ErrorReporterFactory import *
from SublimeGHCi.completions.defaults import *
from SublimeGHCi.controllers.ControllerManager import *
from SublimeGHCi.controllers.defaults import *
from SublimeGHCi.ghci.defaults import *
from SublimeGHCi.projects.defaults import *
from SublimeGHCi.output_panels.OutputPanelFactory import *

manager = None

@save_integ_exceptions
def wire_everything_together():
	global manager

	output_panel_factory = OutputPanelFactory()

	project_manager = default_project_manager()
	error_reporter_factory = ErrorReporterFactory(project_manager, output_panel_factory)
	ghci_connection_factory = default_ghci_connection_factory(project_manager, error_reporter_factory)
	ghci_factory = default_ghci_factory(ghci_connection_factory)
	completor_factory = default_completor_factory(ghci_factory)

	controller_factory = default_controller_factory(ghci_factory, completor_factory)
	manager = ControllerManager(controller_factory)

wire_everything_together()

@save_integ_exceptions
def plugin_loaded():
	pass

@save_integ_exceptions
def plugin_unloaded():
	print("terminating ghci")
	#manager.remove_all()

class HooksListener(sublime_plugin.EventListener):
	@save_integ_exceptions
	def on_post_save(self, view):
		manager.saved(view)

	@save_integ_exceptions
	def on_setting_changed(self):
		print('setting changed')

	@save_integ_exceptions
	def on_query_completions(self, view, prefix, locations):
		return manager.complete(view, prefix, locations[0])

	@save_integ_exceptions
	def on_new(self, view):
		manager.add(view)

	@save_integ_exceptions
	def on_activated(self, view):
		manager.add(view)

	@save_integ_exceptions
	def on_load(self, view):
		manager.add(view)

	@save_integ_exceptions
	def on_close(self, view):
		manager.close(view)