from projects.Project import *

class ProjectManager(object):
	def __init__(self, window_info):
		self._window_info = window_info

	def project_for_view(self, view):
		if len(self._window_info.folders()) == 0:
			return Project('ghci', 'a/b')
		else:
			return Project('ghci', 'a')