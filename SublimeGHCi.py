import sublime, sublime_plugin, subprocess, re
from SublimeGHCi.OutputPanel import OutputPanel
from SublimeGHCi.GHCiConnection import *
from SublimeGHCi.GHCiCommands import *
from SublimeGHCi.LoadedGHCiCommands import *

ghci_connection = GHCiConnection()
ghci = LoadedGHCiCommands(ghci_connection, GHCiCommands(ghci_connection))
output_panel = OutputPanel('sublime_ghci')

def is_haskell_source_file(file_name):
	return re.search(r'\.l?hs$', file_name) != None

def plugin_loaded():
	pass

def plugin_unloaded():
	print("terminating ghci")
	ghci_connection.terminate()

class HooksListener(sublime_plugin.EventListener):
	def on_post_save(self, view):
		if not is_haskell_source_file(view.file_name()):
			return
		
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
		cs = [ (x + '\t' + ghci.type_or_kind_of(x).value(), x) for x in ghci.completions(prefix) ]
		print(cs)
		return cs
