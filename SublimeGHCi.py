import sublime, sublime_plugin, subprocess, re

sp = subprocess.Popen("/usr/local/bin/ghci", stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)

autocompletions = []

prompt_repeating_part = b']]]]]]]]]]]]]]]]'
prompt = prompt_repeating_part + prompt_repeating_part[:-1]

def read_until_prompt():
	data = b''
	while True:
		read = sp.stdout.read(len(prompt_repeating_part))
		if read == prompt_repeating_part:
			break
		data += read
	string = data.decode('utf-8')
	return re.sub(r'^\]*([^\]]+)\]*$', r'\1', string)

def message_gchi(msg):
	sp.stdin.write(msg + b'\n')
	sp.stdin.flush()
	return read_until_prompt()

def clearBeginning():
	print(sp.stdout.read1(100000))
	print(message_gchi(b':set prompt ' + prompt))

def plugin_loaded():
	sublime.set_timeout(clearBeginning, 2000)

def plugin_unloaded():
	print("terminating ghci")
	sp.terminate()

class ExampleCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.insert(edit, 0, "Hello, World!")

class HooksListener(sublime_plugin.EventListener):
	def on_post_save(self, view):
		completions = message_gchi(b':complete repl 10 ""')
		print(completions)

	def on_query_completions(self, view, prefix, locations):
		pass
