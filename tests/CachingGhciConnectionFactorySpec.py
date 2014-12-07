import unittest
from unittest.mock import *

from SublimeGHCi.ghci.CachingGhciFactory import *

class GhciCommands(object):
	pass

class GhciFactory(object):
	def new_ghci_for_view(self, view):
		return GhciCommands()

class View(object):
	pass

class CachingGhciFactorySpec(unittest.TestCase):
	def setUp(self):
		self.caching_factory = CachingGhciFactory(GhciFactory())

	def test_when_asked_for_the_different_ghci_views_twice_it_should_return_different_values(self):
		first = self.caching_factory.new_ghci_for_view(View())
		second = self.caching_factory.new_ghci_for_view(View())
		return self.assertNotEqual(first, second)

	def test_when_asked_for_the_same_ghci_view_twice_it_should_return_the_same_value(self):
		view = View()
		first = self.caching_factory.new_ghci_for_view(view)
		second = self.caching_factory.new_ghci_for_view(view)
		return self.assertEqual(first, second)