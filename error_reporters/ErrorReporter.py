import sublime, re

from SublimeGHCi.Common import find_open_file
from SublimeGHCi.output_panels.OutputPanel import OutputPanel
from SublimeGHCi.Highlights import ErrorHighlights

class ErrorPos(object):
	def __init__(self, view, region):
		self._view = view
		self._region = region

	@staticmethod
	def to_end_of_line(file_name, row, col):
		view = find_open_file(file_name)
		start = view.text_point(row, col)
		line = view.line(start)
		region = sublime.Region(start, line.end())
		return ErrorPos(view, region)

	def view(self):
		return self._view

	def region(self):
		return self._region

def absolute_path(path, root_directory):
	if path.startswith('/'):
		return path
	else:
		return '{}/{}'.format(root_directory, path)

def files_compiled(str, project_directory):
	matches = re.finditer(r'\] Compiling .*?\( (.*?),', str)
	possibly_relative_paths = map(lambda match: match.group(1), matches)
	paths = map(lambda path: absolute_path(path, project_directory), possibly_relative_paths)
	return set(paths)

def match_to_error_pos(match, project_directory):
	file_name = absolute_path(match.group(1), project_directory)
	row = int(match.group(2)) - 1
	col = int(match.group(3)) - 1
	return ErrorPos.to_end_of_line(file_name, row, col)

def parse_errors(error_message, project_directory):
	matches = re.finditer(r'(.*?):(\d+):(\d+):\n', error_message)
	return list(map(lambda match: match_to_error_pos(match, project_directory), matches))

class ErrorReporter(object):
	def __init__(self):
		self._output_panel = OutputPanel(sublime.active_window())
		self._error_highlights = ErrorHighlights()

	def report_errors(self, error_message, project_directory):
		self._output_panel.display_text(error_message)
		error_positions = parse_errors(error_message, project_directory)
		compiled = files_compiled(error_message, project_directory)
		successful = compiled.difference(map(lambda ep: ep.view().file_name(), error_positions))
		print(successful)
		self._error_highlights.highlight(error_positions)

	def clear_errors(self):
		self._output_panel.hide()
		self._error_highlights.erase()
		pass

class NullErrorReporter(object):
	def report_errors(self, error_message, project_directory):
		pass

	def clear_errors(self):
		pass