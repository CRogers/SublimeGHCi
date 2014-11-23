import os

from projects.Project import *

class ProjectManager(object):
	def __init__(self, window_info, project_file_detector):
		self._window_info = window_info
		self._project_file_detector = project_file_detector

	def _get_deepest_folder(self, folders, directory_of_view):
		deepest_folder_prefix_len = 0
		deepest_folder = None
		for folder_data in folders:
			prefix = os.path.commonprefix([folder_data.folder(), directory_of_view])
			if len(prefix) > deepest_folder_prefix_len:
				deepest_folder_prefix_len = len(prefix)
				deepest_folder = folder_data

		return deepest_folder

	def project_for_view(self, view):
		folders = self._window_info.folders()
		directory_of_view = os.path.dirname(view.file_name())
		folders_view_is_in = list(filter(lambda folder_data: directory_of_view.startswith(folder_data.folder()), folders))
		if len(folders_view_is_in) == 0:
			return GhciProject(directory_of_view)
		
		deepest_folder = self._get_deepest_folder(folders_view_is_in, directory_of_view)
		
		if deepest_folder.has_project_data():
			return CustomProject(deepest_folder.folder(), deepest_folder.project_data())

		project = GhciProject(deepest_folder.folder())
		if self._project_file_detector.has_cabal_file(deepest_folder.folder()):
			project = CabalProject(deepest_folder.folder())

		if self._project_file_detector.has_default_nix_file(deepest_folder.folder()):
			project = NixProject(project)

		return project