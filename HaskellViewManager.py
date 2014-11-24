import re

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.ErrorReporter import ErrorReporter, ErrorHighlights
from SublimeGHCi.HaskellView import HaskellView

def key(view):
	return view.id()

def is_haskell_source_file(file_name):
	if file_name == None:
		return False
	
	return re.search(r'\.l?hs$', file_name) != None

class HaskellViewManager(object):
	def __init__(self):
		self.__views = dict()
		self.__error_reporter = ErrorReporter()
		self.__test_highlights = ErrorHighlights()

	def exists(self, view):
		return key(view) in self.__views

	def add(self, view):
		already_added = self.exists(view)
		if already_added or not is_haskell_source_file(view.file_name()):
			return

		print('creating new ghci for {}'.format(view.file_name()))
		self.__views[key(view)] = HaskellView(view, self.__error_reporter, self.__test_highlights)

	def __remove(self, k):
		self.__views[k].close()
		del self.__views[k]

	def remove(self, view):
		if not self.exists(view):
			return

		self.__remove(key(view))

	def remove_all(self):
		for k in list(self.__views):
			self.__remove(k)

	def __ghci_for(self, view):
		if not self.exists(view):
			return Fallible.fail(None)
		else:
			return Fallible.succeed(self.__views[key(view)])

	def saved(self, view):
		self.__ghci_for(view).map(lambda haskell_view: haskell_view.saved())

	def completions(self, view, prefix):
		return (self.__ghci_for(view)
			.bind(lambda haskell_view: haskell_view.completions(prefix))
			.map_fail(lambda _: []))