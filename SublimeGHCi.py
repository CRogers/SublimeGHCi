import sublime, sublime_plugin, subprocess, re
from SublimeGHCi.OutputPanel import OutputPanel

sp = subprocess.Popen("/usr/local/bin/ghci", stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)

autocompletions = []

prompt_repeating_part = b']]]]]]]]]]]]]]]]'
prompt = (prompt_repeating_part + prompt_repeating_part[:-1]).decode('utf-8')

output_panel = OutputPanel('sublime_ghci')

def read_until_prompt():
	data = b''
	while True:
		read = sp.stdout.read(len(prompt_repeating_part))
		if read == prompt_repeating_part:
			break
		data += read
	string = data.decode('utf-8')
	return re.sub(r'^\]*((.|\n)+)\n\]*$', r'\1', string)

def message_gchi(msg):
	sp.stdin.write(msg.encode('utf-8') + b'\n')
	sp.stdin.flush()
	return read_until_prompt()

def clearBeginning():
	print(sp.stdout.read1(1000000))
	print(message_gchi(':set prompt ' + prompt))

def is_haskell_source_file(file_name):
	return re.search(r'\.l?hs$', file_name) != None

def plugin_loaded():
	return sublime.set_timeout(clearBeginning, 2000)

def plugin_unloaded():
	print("terminating ghci")
	sp.terminate()

def get_last_part(sig):
	return re.match(r'([A-Z].*?\.)*(.*)$', sig).group(2)

def get_completions(prefix = ''):
	msg = ':complete repl 1000000 "{}"'.format(prefix)
	lines = message_gchi(msg).split('\n')[1:]
	completions = [re.sub(r'"(.*)"', r'\1', line) for line in lines if line != '']
	return completions

def get_info_part(str):
	return re.sub(r'^.* :: (.*?)$', r'\1', str)

def is_not_defined(str):
	return re.search(r'Not in scope', str) != None

def get_type(expr):
	msg = ':t ({})'.format(expr)
	response = message_gchi(msg)
	if is_not_defined(response):
		return ''
	return get_info_part(response)

def get_kind(expr):
	msg = ':k ({})'.format(expr)
	response = message_gchi(msg)
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
	response = message_gchi(msg)
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
