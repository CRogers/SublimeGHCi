class ControllerManager(object):
	def __init__(self, controller_factory):
		self._controller_factory = controller_factory

	def add(self, view):
		is_hs = view.file_name()[-3:] == '.hs'
		is_lhs = view.file_name()[-4:] == '.lhs'
		if is_hs or is_lhs:
			self._controller_factory.controller_for_view(view)