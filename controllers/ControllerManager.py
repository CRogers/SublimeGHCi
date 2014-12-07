class ControllerManager(object):
	def __init__(self, controller_factory):
		self._controller_factory = controller_factory

	def add(self, view):
		if view.file_name()[-3:] == '.hs':
			self._controller_factory.controller_for_view(view)