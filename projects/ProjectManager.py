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
		
		deepest_folder_prefix_len = 0
		deepest_folder = None
		for folder in folders_view_is_in:
			prefix = os.path.commonprefix([folder, directory_of_view])
			if len(prefix) > deepest_folder_prefix_len:
				deepest_folder_prefix_len = len(prefix)
				deepest_folder = folder

		return Project('ghci', deepest_folder)