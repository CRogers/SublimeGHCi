import os

from projects.Project import *

class ProjectManager(object):
	def __init__(self, window_info):
		self._window_info = window_info

	def project_for_view(self, view):
		folders = self._window_info.folders()
		directory_of_view = os.path.dirname(view.file_name())
		folders_view_is_in = list(filter(lambda folder: directory_of_view.startswith(folder), folders))
		if len(folders_view_is_in) == 0:
			return Project('ghci', directory_of_view)
		
		if len(folders) == 2:
			return Project('ghci', 'a/b')

		return Project('ghci', 'a')