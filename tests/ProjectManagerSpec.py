import unittest
from projects.ProjectManager import *

class WindowInfoShim(object):
	def __init__(self):
		self._folders = []

	def folders(self):
		return self._folders;

class ProjectManager_projects_for_view_Spec(unittest.TestCase):
	def setUp(self):
		self.project_manager = ProjectManager()

	def test_should_return_project_with_raw_ghci_for_file_when_there_are_no_folders(self):
		project = self.project_manager.project_for_view(None)
		self.assertEqual(project.ghci_command(), 'ghci')