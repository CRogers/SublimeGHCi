from SublimeGHCi.Settings import Settings

class GHCiFactory(object):
	def __init__(self):
		self.__ghcis = dict()

	def create(self, view, on_loaded):
		if not view.file_name() in self.__ghcis:
			settings = Settings(view)
			ghci = SharedGHCi(LoadedGHCiCommands(GHCiCommands(GHCiConnection(settings, on_loaded))))
			self.__ghcis[view.file_name()] = ghci
		ghci = self.__ghcis[view.file_name()]
		ghci.open()
		return ghci