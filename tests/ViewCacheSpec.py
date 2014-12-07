import unittest
from unittest.mock import *

from SublimeGHCi.common.ViewCache import *

class View(object):
	buffer_count = 0

	def __init__(self):
		self._id = View.buffer_count
		View.buffer_count += 1

	def buffer_id(self):
		return self._id

class Obj(object):
	pass

def new_obj(view):
	return Obj()

class ViewCacheSpec(unittest.TestCase):
	def setUp(self):
		self.view_cache = ViewCache(new_obj)

	def test_when_asked_for_a_view_that_does_not_currently_exist_in_the_cache_it_should_make_a_new_one_and_return_it(self):
		obj = self.view_cache.get_for_view(View())
		self.assertTrue(type(obj) is Obj)