import unittest
from unittest.mock import *

from SublimeGHCi.controllers.ControllerManager import *

class Controller(object):
	pass

class ControllerFactory(object):
	def __init__(self):
		self.controller_for_view = Mock(return_value=Controller())

class View(object):
	def __init__(self, file_name):
		self.file_name = Mock(return_value=file_name)

class ControllerManagerSpec(unittest.TestCase):
	def setUp(self):
		self.factory = ControllerFactory()
		self.controller_manager = ControllerManager(self.factory)

	def test_when_add_is_called_with_a_non_haskell_file_the_factory_is_not_called(self):
		self.controller_manager.add(View('kittens.notahaskellfile'))
		self.assertEqual(self.factory.controller_for_view.call_count, 0)

	def test_when_add_is_called_with_a_hs_extension_it_calls_the_factory(self):
		view = View('kittens.hs')
		self.controller_manager.add(view)
		self.factory.controller_for_view.assert_called_once_with(view)

	