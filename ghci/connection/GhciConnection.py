from SublimeGHCi.common.EventHook import *
from SublimeGHCi.ghci.connection.LoadingGhciConnection import *

class GhciConnection(object):
	def __init__(self, subprocess, os, threading, project):
		self._current = LoadingGhciConnection(subprocess, os, threading, project)
		self._register()
		self._on_loaded = EventHook()

	def _next(self):
		return self._current.next

	def _unregister(self):
		self._next().unregister(self._on_next)

	def _register(self):
		self._next().register(self._on_next)

	def _on_next(self, next_connection):
		self._unregister()
		self._current = next_connection
		self._register()
		if self.loaded():
			self._on_loaded.fire()

	def on_loaded(self):
		return self._on_loaded

	def message(self, msg):
		return self._current.message(msg)

	def loaded(self):
		return self._current.loaded()

	def terminate(self):
		self._current.terminate()