import os

from projects.Project import *

class ProjectManager(object):
	def __init__(self, window_info, project_file_detector):
		self._window_info = window_info
		self._project_file_detector = project_file_detector

	def _get_deepest_folder(self, folders, directory_of_view):
		deepest_folder_prefix_len = 0
		deepest_folder = None
		for folder in folders:
			prefix = os.path.commonprefix([folder, directory_of_view])
			if len(prefix) > deepest_folder_prefix_len:
				deepest_folder_prefix_len = len(prefix)
				deepest_folder = folder

		return deepest_folder

	def project_for_view(self, view):
		folders = self._window_info.folders()
		directory_of_view = os.path.dirname(view.file_name())
		folders_view_is_in = list(filter(lambda folder: directory_of_view.startswith(folder), folders))
		if len(folders_view_is_in) == 0:
			return Project('ghci', directory_of_view)
		
		deepest_folder = self._get_deepest_folder(folders_view_is_in, directory_of_view)
		if self._project_file_detector.has_cabal_file(deepest_folder):
			return Project('cabal repl', deepest_folder)

		return Project('ghci', deepest_folder)