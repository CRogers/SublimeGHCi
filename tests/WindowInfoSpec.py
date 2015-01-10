import unittest
from unittest.mock import *

from SublimeGHCi.projects.WindowInfo import *
from SublimeGHCi.projects.FolderProjectData import *

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

    def test_when_there_is_one_window_with_a_folder_and_no_project_settings_then_there_should_be_one_folder(self):
        self.windows.return_value = [SublimeWindow(folders=['a'])]
        folders = self.window_info.folders()
        self.assertEqual(folders, [FolderProjectData('a')])

    def test_when_there_is_one_window_with_two_folders_and_no_project_settings_then_there_should_be_two_folders(self):
        self.windows.return_value = [SublimeWindow(folders=['a', 'b'])]
        folders = self.window_info.folders()
        self.assertEqual(folders, [FolderProjectData('a'), FolderProjectData('b')])

    def test_when_there_is_one_window_with_one_folder_and_project_settings_the_outputted_folder_should_have_the_settings(self):
        settings = {}
        self.windows.return_value = [SublimeWindow(folders=['a'], project_data={'settings': settings})]
        folders = self.window_info.folders()
        self.assertEqual(folders, [FolderProjectData('a', settings)])

    def test_when_there_is_one_window_with_two_folders_and_project_settings_the_outputted_folders_should_have_the_settings(self):
        settings = {}
        self.windows.return_value = [SublimeWindow(folders=['a', 'b'], project_data={'settings': settings})]
        folders = self.window_info.folders()
        self.assertEqual(folders, [FolderProjectData('a', settings), FolderProjectData('b', settings)])

    def test_when_there_are_two_windows_with_one_folder_each_and_no_project_settings_those_folders_are_outputted(self):
        self.windows.return_value = [SublimeWindow(folders=['a']), SublimeWindow(folders=['b'])]
        folders = self.window_info.folders()
        self.assertEqual(folders, [FolderProjectData('a'), FolderProjectData('b')])

    def test_when_there_are_two_windows_with_one_folder_each_and_only_one_with_project_settings_those_folders_are_outputted(self):
        settings = {}
        window1 = SublimeWindow(folders=['a'], project_data={'settings': settings})
        self.windows.return_value = [window1, SublimeWindow(folders=['b'])]
        folders = self.window_info.folders()
        self.assertEqual(folders, [FolderProjectData('a', settings), FolderProjectData('b')])

    def test_when_there_are_two_windows_with_one_folder_each_and_both_with_project_settings_those_folders_are_outputted(self):
        settings1 = {'foo': 'bar'}
        window1 = SublimeWindow(folders=['a'], project_data={'settings': settings1})
        settings2 = {'baz': 'quux'}
        window2 = SublimeWindow(folders=['b'], project_data={'settings': settings2})
        self.windows.return_value = [window1, window2]
        folders = self.window_info.folders()
        self.assertEqual(folders, [FolderProjectData('a', settings1), FolderProjectData('b', settings2)])