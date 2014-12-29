import sublime_plugin

from SublimeGHCi.ErrorReporter import *
from SublimeGHCi.completions.defaults import *
from SublimeGHCi.controllers.ControllerManager import *
from SublimeGHCi.controllers.defaults import *
from SublimeGHCi.ghci.defaults import *
from SublimeGHCi.projects.defaults import *

error_reporter = ErrorReporter()

project_manager = default_project_manager()
ghci_connection_factory = default_ghci_connection_factory(project_manager, error_reporter)
ghci_factory = default_ghci_factory(ghci_connection_factory)
completor_factory = default_completor_factory(ghci_factory)

controller_factory = default_controller_factory(project_manager, ghci_factory, completor_factory, error_reporter)
manager = ControllerManager(controller_factory)

def plugin_loaded():
	pass

def plugin_unloaded():
	print("terminating ghci")
	#manager.remove_all()

class HooksListener(sublime_plugin.EventListener):
	def on_post_save(self, view):
		manager.saved(view)

	def on_setting_changed(self):
		print('setting changed')

	def on_query_completions(self, view, prefix, locations):
		return manager.complete(view, prefix, locations[0])

	def on_new(self, view):
		manager.add(view)

	def on_activated(self, view):
		manager.add(view)

	def on_load(self, view):
		manager.add(view)

	def on_close(self, view):
		manager.close(view)