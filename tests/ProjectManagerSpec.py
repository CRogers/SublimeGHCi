import unittest
from projects.ProjectManager import *

class WindowInfoShim(object):
	def __init__(self):
		self._folders = []

	def folders(self):
		return self._folders

class ProjectFileDetectorShim(object):
	def __init__(self):
		self._has_cabal_file = False

	def has_cabal_file(self, path):
		return self._has_cabal_file

class ViewShim(object):
	def __init__(self, file_name):
		self._file_name = file_name

	def file_name(self):
		return self._file_name

class ProjectManager_projects_for_view_Spec(unittest.TestCase):
	def setUp(self):
		self.window_info = WindowInfoShim()
		self.project_file_detector = ProjectFileDetectorShim()
		self.project_manager = ProjectManager(self.window_info, self.project_file_detector)

	def test_should_return_project_with_raw_ghci_for_file_when_there_are_no_folders(self):
		view = ViewShim('foo.hs')
		project = self.project_manager.project_for_view(view)
		self.assertEqual(project.ghci_command(), 'ghci')

	def test_the_base_path_for_a_lone_haskell_file_should_be_the_directory_of_the_file(self):
		view = ViewShim('a/b/c.hs')
		project = self.project_manager.project_for_view(view)
		self.assertEqual(project.base_path(), 'a/b')

	def test_when_there_is_a_folder_but_the_file_isnt_in_it_the_base_path_should_be_the_directory_of_the_file(self):
		view = ViewShim('a/b/c.hs')
		self.window_info._folders = ['xyz']
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

	def test_when_the_file_is_within_three_folders_the_base_path_should_be_the_deepest_folder(self):
		view = ViewShim('w/x/y/z.hs')
		self.window_info._folders = ['w', 'w/x', 'w/x/y']
		project = self.project_manager.project_for_view(view)
		self.assertEqual(project.base_path(), 'w/x/y')

	def test_when_there_is_a_cabal_file_in_the_files_directory_use_cabal_repl(self):
		view = ViewShim('a/b.hs')
		self.window_info._folders = ['a']
		self.project_file_detector._has_cabal_file = True
		project = self.project_manager.project_for_view(view)
		self.assertEqual(project.ghci_command(), 'cabal repl')


