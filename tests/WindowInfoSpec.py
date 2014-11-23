import unittest
from unittest.mock import *

from SublimeGHCi.projects.WindowInfo import *

class Sublime(object):
	pass

class SublimeWindow(object):
	def __init__(self, project_data={}, folders=[]):
		self.project_data = Mock(return_value=project_data)
		self.folders = Mock(return_value=folders)

class WindowInfoSpec(unittest.TestCase):
	def setUp(self):
		self.windows = Mock(return_value=[])
		sublime = Sublime()
		sublime.windows = self.windows
		self.window_info = WindowInfo(sublime)

	def test_when_there_are_no_windows_there_should_be_no_folders(self):
		folders = self.window_info.folders()
		self.assertEqual(folders, [])

	def test_when_there_is_one_window_with_no_folders_and_no_project_settings_there_should_be_no_folders(self):
		self.windows.return_value = [SublimeWindow()]
		folders = self.window_info.folders()
		self.assertEqual(folders, [])