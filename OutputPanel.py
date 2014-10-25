import sublime, sublime_plugin, uuid

class SublimeGhciOutputText(sublime_plugin.TextCommand):
	def run(self, edit, text = None):
		if text == None:
			return
		print('edit ' + text)
		self.view.erase(edit, sublime.Region(0, self.view.size()))
		self.view.insert(edit, 0, text)

class OutputPanel(object):
	def __init__(self):
		self.__name = str(uuid.uuid4())
		self.__output_panel = None

	def __create_output_panel(self):
		self.__output_panel = sublime.active_window().create_output_panel(self.__name)

	def __get_view(self):
		if self.__output_panel == None:
			self.__create_output_panel()
		return self.__output_panel

	def display_text(self, text):
		view = self.__get_view()
		view.set_read_only(False)
		view.run_command('sublime_ghci_output_text', {'text': text})
		view.set_read_only(True)
		self.show()

	def __runCommandWithPanel(self, command):
		sublime.active_window().run_command(command, {'panel': 'output.' + self.__name})

	def show(self):
		self.__runCommandWithPanel('show_panel')

	def hide(self):
		self.__runCommandWithPanel('hide_panel')