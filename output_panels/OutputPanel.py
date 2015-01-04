import sublime, sublime_plugin, uuid

class SublimeGhciOutputText(sublime_plugin.TextCommand):
	def run(self, edit, text = None):
		if text == None:
			return
		self.view.erase(edit, sublime.Region(0, self.view.size()))
		self.view.insert(edit, 0, text)

output_panels = []

class OutputPanel(object):
	def __init__(self, window):
		self._window = window
		self._name = str(uuid.uuid4())
		self._output_panel = None

	def _create_output_panel(self):
		self._output_panel = self._window.create_output_panel(self._name)
		output_panels.append(self._output_panel)

	# Exposed for testing
	def get_view(self):
		if self._output_panel == None:
			self._create_output_panel()
		return self._output_panel

	def display_text(self, text):
		view = self.get_view()
		view.set_read_only(False)
		view.run_command('sublime_ghci_output_text', {'text': text})
		view.set_read_only(True)
		self.show()

	def _runCommandWithPanel(self, command):
		sublime.active_window().run_command(command, {'panel': 'output.' + self._name})

	def show(self):
		self._runCommandWithPanel('show_panel')

	def hide(self):
		self._runCommandWithPanel('hide_panel')