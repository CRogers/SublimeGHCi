class ControllerManager(object):
	def __init__(self, controller_factory):
		self._controller_factory = controller_factory

	def _call_if_haskell_file(self, view, func):
		file_name = view.file_name()
		if file_name == None:
			return
		is_hs = file_name[-3:] == '.hs'
		is_lhs = file_name[-4:] == '.lhs'
		if is_hs or is_lhs:
			controller = self._controller_factory.controller_for_view(view)
			return func(controller)

	def _call_attr_if_haskell_file(self, view, funcName, *args):
		return self._call_if_haskell_file(view, lambda controller: getattr(controller, funcName)(*args))

	def loaded(self, view):
		loaded = self._call_attr_if_haskell_file(view, 'loaded')
		if loaded == None:
			return True
		return loaded

	def add(self, view):
		self._call_if_haskell_file(view, lambda _: None)

	def saved(self, view):
		self._call_attr_if_haskell_file(view, 'saved')

	def complete(self, view, prefix, location):
		return self._call_attr_if_haskell_file(view, 'complete', prefix, location)

	def close(self, view):
		self._call_attr_if_haskell_file(view, 'close')