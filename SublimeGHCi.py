import sublime, sublime_plugin, subprocess, re
from SublimeGHCi.OutputPanel import OutputPanel
from SublimeGHCi.GHCiConnection import *
from SublimeGHCi.GHCiCommands import *

ghci_connection = GHCiConnection()
ghci = GHCiCommands(ghci_connection)
output_panel = OutputPanel('sublime_ghci')

def is_haskell_source_file(file_name):
	return re.search(r'\.l?hs$', file_name) != None

def plugin_loaded():
	return sublime.set_timeout(ghci_connection.consume_beginning, 2000)

def plugin_unloaded():
	print("terminating ghci")
	sp.terminate()

def has_failed(response):
	return re.search(r'Failed, modules loaded:', response) != None

class HooksListener(sublime_plugin.EventListener):
	def on_post_save(self, view):
		if not is_haskell_source_file(view.file_name()):
			return
		response = ghci.load_haskell_file(view.file_name())
		if has_failed(response):
			output_panel.display_text(response)
		else:
			output_panel.hide()

	def on_setting_changed(self):
		print('setting changed')

	def on_query_completions(self, view, prefix, locations):
		if not is_haskell_source_file(view.file_name()):
			return []
		cs = [ (x + '\t' + ghci.get_type_or_kind(x), x) for x in ghci.completions(prefix) ]
		print(cs)
		return cs
