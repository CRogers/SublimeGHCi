class FolderProjectData(object):
	def __init__(self, folder, project_data=None):
		self._folder = folder
		self._project_data = project_data

	def folder(self):
		return self._folder

	def has_project_data(self):
		return self._project_data != None

	def project_data(self):
		return self._project_data