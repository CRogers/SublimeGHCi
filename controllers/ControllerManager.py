class ControllerManager(object):
	def __init__(self, controller_factory):
		self._controller_factory = controller_factory

	def add(self, view):
		pass