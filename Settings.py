import sublime, os

class Settings(object):
	def __init__(self, view):
		self.__view = view
		self.__settings = view.settings()

	def ghci_command(self):
		return self.__settings.get('ghci_command')

	def __ghci_test(self):
		return self.__settings.get('ghci_test')

	def test_module(self):
		return self.__ghci_test()['module']

	def test_command(self):
		return self.__ghci_test()['command']

	def project_directory(self):
		project_file = self.__view.window().project_file_name()
		if project_file == None:
			return None
		return os.path.dirname(project_file)