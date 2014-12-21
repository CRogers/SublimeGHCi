import sublime_plugin

class InsertText(sublime_plugin.TextCommand):
	def run(self, edit, point=0, string=''):
		self.view.insert(edit, point, string)