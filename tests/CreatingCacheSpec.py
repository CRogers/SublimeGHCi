import unittest
from unittest.mock import *

from SublimeGHCi.common.CreatingCache import *

class KeyObject(object):
	count = 0

	def __init__(self):
		self._id = KeyObject.count
		KeyObject.count += 1

	def id(self):
		return self._id

class Obj(object):
	def __init__(self, *args):
		pass

class CreatingCacheSpec(unittest.TestCase):
	def setUp(self):
		self.new_obj = Mock(side_effect=Obj)
		self.key_func = Mock(side_effect = lambda x: x.id())
		self.cache = CreatingCache(self.new_obj, self.key_func)

	def test_when_asked_for_a_key_object_that_does_not_currently_exist_in_the_cache_it_should_make_a_new_one_and_return_it(self):
		obj = self.cache.get(KeyObject())
		self.assertTrue(type(obj) is Obj)

	def test_when_creating_a_new_obj_that_it_should_pass_the_view_to_the_creation_function(self):
		key_object = KeyObject()
		self.cache.get(key_object)
		self.new_obj.assert_called_once_with(key_object)

	def test_when_asking_twice_with_two_different_views_different_objs_are_returned(self):
		first = self.cache.get(KeyObject())
		second = self.cache.get(KeyObject())
		self.assertNotEqual(first, second)

	def test_when_asking_twice_with_the_same_view_the_same_obj_is_returned(self):
		key_object = KeyObject()
		first = self.cache.get(key_object)
		second = self.cache.get(key_object)
		self.assertEqual(first, second)