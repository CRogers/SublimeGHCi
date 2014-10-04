import sublime, sublime_plugin, subprocess, re
from SublimeGHCi.ViewGHCis import ViewGHCis

view_ghcis = ViewGHCis()

def plugin_loaded():
	pass

def plugin_unloaded():
	print("terminating ghci")
	view_ghcis.remove_all()

class HooksListener(sublime_plugin.EventListener):
	def on_post_save(self, view):
		view_ghcis.saved(view)

	def on_setting_changed(self):
		print('setting changed')

	def on_query_completions(self, view, prefix, locations):
		completions = view_ghcis.completions(view, prefix).value()
		print(completions)
		return completions

	def on_new(self, view):
		#print('new view {} created'.format(view.file_name()))
		view_ghcis.add(view)

	def on_activated(self, view):
		#print('view {} activated'.format(view.file_name()))
		view_ghcis.add(view)

	def on_load(self, view):
		#print('loaded view {}'.format(view.file_name()))
		view_ghcis.add(view)

	def on_close(self, view):
		#print('view {} closed'.format(view.file_name()))
		view_ghcis.remove(view)