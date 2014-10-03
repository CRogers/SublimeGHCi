import sublime, sublime_plugin, subprocess, re
from SublimeGHCi.OutputPanel import OutputPanel
from SublimeGHCi.ViewGHCis import ViewGHCis

view_ghcis = ViewGHCis()
output_panel = OutputPanel('sublime_ghci')

def is_haskell_source_file(file_name):
	return re.search(r'\.l?hs$', file_name) != None

def plugin_loaded():
	pass

def plugin_unloaded():
	print("terminating ghci")
	view_ghcis.remove_all()

class HooksListener(sublime_plugin.EventListener):
	def on_post_save(self, view):
		if not is_haskell_source_file(view.file_name()):
			return
		ghci = view_ghcis.ghci_for(view)

		ghci.load_haskell_file(view.file_name()) \
			.switch(
				lambda _: output_panel.hide(),
				output_panel.display_text
			)

	def on_setting_changed(self):
		print('setting changed')

	def on_query_completions(self, view, prefix, locations):
		if not is_haskell_source_file(view.file_name()):
			return []
		ghci = view_ghcis.ghci_for(view)
		cs = [ (x + '\t' + ghci.type_or_kind_of(x).value(), x) for x in ghci.completions(prefix) ]
		print(cs)
		return cs

	def on_new(self, view):
		print('new view {} created'.format(view.file_name()))
		view_ghcis.add(view)

	def on_activated(self, view):
		print('view {} activated'.format(view.file_name()))
		view_ghcis.add(view)

	def on_load(self, view):
		print('loaded view {}'.format(view.file_name()))
		view_ghcis.add(view)

	def on_close(self, view):
		print('view {} closed'.format(view.file_name()))
		view_ghcis.remove(view)