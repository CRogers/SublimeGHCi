import unittest
from unittest.mock import *

from SublimeGHCi.ghci.GhciFactory import *
from SublimeGHCi.projects.Project import GhciProject

class ProjectManager(object):
	def __init__(self):
		self.project_for_view = Mock(return_value=GhciProject('/tmp/'))

class View(object):
	def __init__(self):
		self.file_name = Mock(return_value='blah.hs')

class GhciFactorySpec(unittest.TestCase):
	def setUp(self):
		self.project_manager = ProjectManager()
		self.ghci_factory = GhciFactory(self.project_manager)

	def test_initialises_properly(self):
		pass