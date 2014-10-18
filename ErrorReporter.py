import sublime, re

from SublimeGHCi.OutputPanel import OutputPanel
from SublimeGHCi.Highlights import ErrorHighlights

class ErrorPos(object):
	def __init__(self, file_name, row, col):
		self.__view = sublime.active_window().find_open_file(file_name)
		start = self.__view.text_point(row, col)
		line = self.__view.line(start)
		self.__region = sublime.Region(start, line.end())

	def view(self):
		return self.__view

	def region(self):
		return self.__region

def absolute_path(path, root_directory):
	if path.startswith('/'):
		return path
	else:
		return '{}/{}'.format(root_directory, path)

def files_compiled(str, project_directory):
	matches = re.finditer(r'\] Compiling .*?\( (.*?),', str)
	possibly_relative_paths = map(lambda match: match.group(1), matches)
	paths = map(lambda path: absolute_path(path, project_directory), possibly_relative_paths)
	return list(paths)

def match_to_error_pos(match):
	file_name = match.group(1)
	row = int(match.group(2)) - 1
	col = int(match.group(3)) - 1
	return ErrorPos(file_name, row, col)

def parse_errors(error_message):
	matches = re.finditer(r'(.*?):(\d+):(\d+):\n', error_message)
	return map(match_to_error_pos, matches)

class ErrorReporter(object):
	def __init__(self):
		self.__output_panel = OutputPanel('sublime_ghci')
		self.__error_highlights = ErrorHighlights()

	def report_errors(self, error_message, project_directory):
		self.__output_panel.display_text(error_message)
		error_positions = parse_errors(error_message)
		print(files_compiled(error_message, project_directory))
		self.__error_highlights.highlight(error_positions)

	def clear_errors(self):
		self.__output_panel.hide()
		self.__error_highlights.erase()
		pass