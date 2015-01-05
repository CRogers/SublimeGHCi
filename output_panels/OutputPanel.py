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
		self._testing_shown = False

	def _create_output_panel(self):
		self._output_panel = self._window.create_output_panel(self._name)
		output_panels.append(self._output_panel)

	def _get_view(self):
		if self._output_panel == None:
			self._create_output_panel()
		return self._output_panel

	def display_text(self, text):
		view = self._get_view()
		view.set_read_only(False)
		view.run_command('sublime_ghci_output_text', {'text': text})
		view.set_read_only(True)
		self.show()

	# Exposed for testing. Do not use when there is the possibility of user interaction
	def _testing_is_shown(self):
		return self._testing_shown

	def _runCommandWithPanel(self, command):
		sublime.active_window().run_command(command, {'panel': 'output.' + self._name})

	def show(self):
		self._testing_shown = True
		self._runCommandWithPanel('show_panel')

	def hide(self):
		self._testing_shown = False
		self._runCommandWithPanel('hide_panel')