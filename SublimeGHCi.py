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
	return re.sub(r'^\]*((.|\n)+)\n\]*$', r'\1', string)

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

def get_completions(prefix = ''):
	msg = ':complete repl 1000000 "{}"'.format(prefix)
	lines = message_gchi(msg.encode('utf-8')).split('\n')[1:]
	completions = [re.sub(r'"(.*)"', r'\1', line) for line in lines if line != '']
	return completions

def get_type(expr):
	response = message_gchi(b':t (' + expr.encode('utf-8') + b')')
	return re.sub(r'^.* :: (.*?)$', r'\1', response)

class ExampleCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.insert(edit, 0, "Hello, World!")

class HooksListener(sublime_plugin.EventListener):
	def on_post_save(self, view):
		completions = get_completions()
		for completion in completions:
			print((completion, get_type(completion)))
		#print(completions)
		#print(get_type(completions[0]))

	def on_query_completions(self, view, prefix, locations):
		cs = [ (x + '\t' + get_type(x), x) for x in get_completions(prefix) ]
		print(cs)
		return cs
