import sublime, sublime_plugin

class SublimeGhciOutputText(sublime_plugin.TextCommand):
	def run(self, edit, text = None):
		if text == None:
			return
		print('edit ' + text)
		self.view.erase(edit, sublime.Region(0, self.view.size()))
		self.view.insert(edit, 0, text)

class OutputPanel(object):
	def __init__(self, name):
		self._name = name
		self._output_panel = None

	def _create_output_panel(self):
		self._output_panel = sublime.active_window().create_output_panel(self._name)

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

	def _runCommandWithPanel(self, command):
		sublime.active_window().run_command(command, {'panel': 'output.' + self._name})

	def show(self):
		self._runCommandWithPanel('show_panel')

	def hide(self):
		self._runCommandWithPanel('hide_panel')