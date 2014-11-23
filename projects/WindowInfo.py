import sublime

from SublimeGHCi.projects.FolderProjectData import *

class WindowInfo(object):
	def folders(self):
		all_folders = []
		for window in sublime.windows():
			func = lambda folder: FolderProjectData(folder, window.project_data())
			folders = map(func, window.folders())
			all_folders.extend(folders)
		return all_folders