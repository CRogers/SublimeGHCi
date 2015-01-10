import unittest
from unittest.mock import *

from SublimeGHCi.projects.ProjectFileDetector import *

class Glob(object):
    pass

class ProjectFileDetectorSpec(unittest.TestCase):
    def setUp(self):
        self._glob = Mock(return_value=[])
        glob = Glob()
        glob.glob = self._glob
        self._project_file_detector = ProjectFileDetector(glob)

    def test_when_no_cabal_files_exists_has_cabal_file_returns_false(self):
        self.assertFalse(self._project_file_detector.has_cabal_file('a'))

    def test_when_one_cabal_file_exist_has_cabal_file_returns_true(self):
        self._glob.return_value = ['a/b.cabal']
        self.assertTrue(self._project_file_detector.has_cabal_file('a'))

    def test_when_two_cabal_files_exists_has_cabal_file_returns_true(self):
        self._glob.return_value = ['a/b.cabal', 'a/c.cabal']
        self.assertTrue(self._project_file_detector.has_cabal_file('a'))

    def test_when_no_default_nix_file_exists_has_default_nix_file_returns_false(self):
        self.assertFalse(self._project_file_detector.has_default_nix_file('a'))

    def test_when_a_default_nix_file_exists_has_default_nix_file_returns_true(self):
        self._glob.return_value = ['a/default.nix']
        self.assertTrue(self._project_file_detector.has_default_nix_file('a'))