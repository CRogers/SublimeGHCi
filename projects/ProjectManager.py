import os

from projects.Project import *

class ProjectManager(object):
	def __init__(self, window_info):
		self._window_info = window_info

	def project_for_view(self, view):
		folders = self._window_info.folders()
		if len(folders) == 0:
			return Project('ghci', os.path.dirname(view.file_name()))
		
		if len(folders) == 2:
			return Project('ghci', 'a/b')

		return Project('ghci', 'a')