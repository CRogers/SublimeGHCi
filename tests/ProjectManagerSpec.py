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
		self.project_manager = ProjectManager()

	def test_should_return_project_with_raw_ghci_for_file_when_there_are_no_folders(self):
		view = ViewShim('foo.hs')
		project = self.project_manager.project_for_view(view)
		self.assertEqual(project.ghci_command(), 'ghci')

	def test_the_base_path_for_a_lone_haskell_file_should_be_the_directory_of_the_file(self):
		view = ViewShim('a/b/c.hs')
		project = self.project_manager.project_for_view(view)
		self.assertEqual(project.base_path(), 'a/b')