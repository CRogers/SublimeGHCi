import unittest
from unittest.mock import *

from SublimeGHCi.projects.WindowInfo import *

class Sublime(object):
	pass

class WindowInfoSpec(unittest.TestCase):
	def setUp(self):
		self.windows = Mock(return_value=[])
		sublime = Sublime()
		sublime.windows = self.windows
		self.window_info = WindowInfo(sublime)

	def test_when_there_are_no_windows_there_should_be_no_folders(self):
		folders = self.window_info.folders()
		self.assertEqual(folders, [])