import sublime
import sublime_plugin

class InsertText(sublime_plugin.TextCommand):
	def run(self, edit, point=0, string=''):
		self.view.insert(edit, point, string)

class SublimeGhciEraseText(sublime_plugin.TextCommand):
	def run(self, edit, start=0, length=0):
		self.view.erase(edit, sublime.Region(start, start + length))