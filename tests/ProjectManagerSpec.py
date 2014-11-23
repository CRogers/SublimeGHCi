import unittest
from projects.ProjectManager import *

class WindowInfoShim(object):
	def __init__(self):
		self._folders = []

	def folders(self):
		return self._folders;

class ViewShim(object):
	def __init__(self, file_name):
		self._file_name = file_name

	def file_name(self):
		return self._file_name

class ProjectManager_projects_for_view_Spec(unittest.TestCase):
	def setUp(self):
		self.window_info = WindowInfoShim()
		self.project_manager = ProjectManager(self.window_info)

	def test_should_return_project_with_raw_ghci_for_file_when_there_are_no_folders(self):
		view = ViewShim('foo.hs')
		project = self.project_manager.project_for_view(view)
		self.assertEqual(project.ghci_command(), 'ghci')

	def test_the_base_path_for_a_lone_haskell_file_should_be_the_directory_of_the_file(self):
		view = ViewShim('a/b/c.hs')
		project = self.project_manager.project_for_view(view)
		self.assertEqual(project.base_path(), 'a/b')

	def test_when_the_file_is_within_a_folder_the_base_path_should_be_that_folder(self):
		view = ViewShim('a/b/c.hs')
		self.window_info._folders = ['a']
		project = self.project_manager.project_for_view(view)
		self.assertEqual(project.base_path(), 'a')

	def test_when_the_file_is_within_two_folders_the_base_path_should_be_the_deepest_folder(self):
		view = ViewShim('a/b/c.hs')
		self.window_info._folders = ['a', 'a/b']
		project = self.project_manager.project_for_view(view)
		self.assertEqual(project.base_path(), 'a/b')
