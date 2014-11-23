import sublime

from SublimeGHCi.projects.FolderProjectData import *

class WindowInfo(object):
	def folders(self):
		all_folders = []
		for window in sublime.windows():
			project_settings = window.project_data().get('settings')
			func = lambda folder: FolderProjectData(folder, project_settings)
			folders = map(func, window.folders())
			all_folders.extend(folders)
		return all_folders