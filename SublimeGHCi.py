import sublime, sublime_plugin, subprocess, re
from SublimeGHCi.HaskellViewManager import HaskellViewManager

manager = HaskellViewManager()

def plugin_loaded():
	pass

def plugin_unloaded():
	print("terminating ghci")
	manager.remove_all()

class HooksListener(sublime_plugin.EventListener):
	def on_post_save(self, view):
		manager.saved(view)

	def on_setting_changed(self):
		print('setting changed')

	def on_query_completions(self, view, prefix, locations):
		print(locations)
		return manager.completions(view, prefix).value()

	def on_new(self, view):
		#print('new view {} created'.format(view.file_name()))
		manager.add(view)

	def on_activated(self, view):
		#print('view {} activated'.format(view.file_name()))
		manager.add(view)

	def on_load(self, view):
		#print('loaded view {}'.format(view.file_name()))
		manager.add(view)

	def on_close(self, view):
		#print('view {} closed'.format(view.file_name()))
		manager.remove(view)