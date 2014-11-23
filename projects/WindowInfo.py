from SublimeGHCi.projects.FolderProjectData import *

class WindowInfo(object):
	def __init__(self, sublime):
		self._sublime = sublime

	def folders(self):
		all_folders = []
		for window in self._sublime.windows():
			project_settings = window.project_data().get('settings')
			func = lambda folder: FolderProjectData(folder, project_settings)
			folders = map(func, window.folders())
			all_folders.extend(folders)
		return all_folders