class GhciProject(object):
	def __init__(self, base_path):
		self._base_path = base_path

	def ghci_command(self):
		return ['ghci']

	def base_path(self):
		return self._base_path

class CabalProject(object):
	def __init__(self, base_path):
		self._base_path = base_path

	def ghci_command(self):
		return ['cabal', 'repl']

	def base_path(self):
		return self._base_path

class NixProject(object):
	def __init__(self, inner_project):
		self._inner_project = inner_project

	def ghci_command(self):
		ghci = self._inner_project.ghci_command()
		return ['nix-shell', '--pure', '--command', "{}".format(' '.join(ghci))]

	def base_path(self):
		return self._inner_project.base_path()

class CustomProject(object):
	def __init__(self, inner_project, project_data):
		self._inner_project = inner_project
		self._project_data = project_data

	def ghci_command(self):
		if 'ghci_command' in self._project_data:
			return self._project_data['ghci_command']
		return self._inner_project.ghci_command()

	def base_path(self):
		return self._inner_project.base_path()