import sublime, sublime_plugin, subprocess, re
from SublimeGHCi.OutputPanel import OutputPanel
from SublimeGHCi.ViewGHCis import ViewGHCis

view_ghcis = ViewGHCis()
output_panel = OutputPanel('sublime_ghci')

def plugin_loaded():
	pass

def plugin_unloaded():
	print("terminating ghci")
	view_ghcis.remove_all()

def autocomplete_entry(ghci, expr):
	return (expr + '\t' + ghci.type_or_kind_of(expr).value(), expr)

class HooksListener(sublime_plugin.EventListener):
	def on_post_save(self, view):
		ghci = view_ghcis.ghci_for(view)
		if ghci.failed():
			return

		(ghci
			.bind(lambda ghci: ghci.load_haskell_file(view.file_name()))
			.map(lambda _: output_panel.hide())
			.mapFail(output_panel.display_text))

	def on_setting_changed(self):
		print('setting changed')

	def on_query_completions(self, view, prefix, locations):
		return (view_ghcis
			.ghci_for(view)
			.bind(lambda ghci: (ghci.completions(prefix)
				.map(lambda completions: [ autocomplete_entry(ghci, x) for x in completions ])))
			.mapFail(lambda _: [])
			.value())

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