from projects.Project import *

class ProjectManager(object):
	def __init__(self, window_info):
		self._window_info = window_info

	def project_for_view(self, view):
		folders = self._window_info.folders()
		num_folders = len(folders)
		if num_folders == 0 or num_folders == 2:
			return Project('ghci', 'a/b')
		else:
			return Project('ghci', 'a')