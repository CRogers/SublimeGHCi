import sublime, sublime_plugin, subprocess, re
from SublimeGHCi.OutputPanel import OutputPanel
from SublimeGHCi.GHCiConnection import *

ghci = GHCiConnection()
output_panel = OutputPanel('sublime_ghci')

def is_haskell_source_file(file_name):
	return re.search(r'\.l?hs$', file_name) != None

def plugin_loaded():
	return sublime.set_timeout(ghci.consume_beginning, 2000)

def plugin_unloaded():
	print("terminating ghci")
	sp.terminate()

def get_last_part(sig):
	return re.match(r'([A-Z].*?\.)*(.*)$', sig).group(2)

def get_completions(prefix = ''):
	msg = ':complete repl 1000000 "{}"'.format(prefix)
	lines = ghci.message(msg).split('\n')[1:]
	completions = [re.sub(r'"(.*)"', r'\1', line) for line in lines if line != '']
	return completions

def get_info_part(str):
	return re.sub(r'^.* :: (.*?)$', r'\1', str)

def is_not_defined(str):
	return re.search(r'Not in scope', str) != None

def get_type(expr):
	msg = ':t ({})'.format(expr)
	response = ghci.message(msg)
	if is_not_defined(response):
		return ''
	return get_info_part(response)

def get_kind(expr):
	msg = ':k ({})'.format(expr)
	response = ghci.message(msg)
	if is_not_defined(response):
		return ''
	return get_info_part(response)

def get_type_or_kind(sig):
	last_part = get_last_part(sig)
	type_ = get_type(sig)
	if type_ == '':
		return get_kind(sig)
	return type_

def has_failed(response):
	return re.search(r'Failed, modules loaded:', response) != None

def load_haskell_file(file_name):
	msg = ':load "{}"'.format(file_name)
	response = ghci.message(msg)
	if has_failed(response):
		output_panel.display_text(response)
	else:
		output_panel.hide()

class HooksListener(sublime_plugin.EventListener):
	def on_post_save(self, view):
		if not is_haskell_source_file(view.file_name()):
			return
		load_haskell_file(view.file_name())

	def on_setting_changed(self):
		print('setting changed')

	def on_query_completions(self, view, prefix, locations):
		if not is_haskell_source_file(view.file_name()):
			return []
		cs = [ (x + '\t' + get_type_or_kind(x), x) for x in get_completions(prefix) ]
		print(cs)
		return cs
