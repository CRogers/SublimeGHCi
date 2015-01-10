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
    def __init__(self, *args):
        pass

class ViewCacheSpec(unittest.TestCase):
    def setUp(self):
        self.new_obj = Mock(side_effect=Obj)
        self.view_cache = ViewCache(self.new_obj)

    def test_when_asked_for_a_view_that_does_not_currently_exist_in_the_cache_it_should_make_a_new_one_and_return_it(self):
        obj = self.view_cache.get_for_view(View())
        self.assertTrue(type(obj) is Obj)

    def test_when_creating_a_new_obj_that_it_should_pass_the_view_to_the_creation_function(self):
        view = View()
        self.view_cache.get_for_view(view)
        self.new_obj.assert_called_once_with(view)

    def test_when_asking_twice_with_two_different_views_different_objs_are_returned(self):
        first = self.view_cache.get_for_view(View())
        second = self.view_cache.get_for_view(View())
        self.assertNotEqual(first, second)

    def test_when_asking_twice_with_the_same_view_the_same_obj_is_returned(self):
        view = View()
        first = self.view_cache.get_for_view(view)
        second = self.view_cache.get_for_view(view)
        self.assertEqual(first, second)