import unittest

from SublimeGHCi.integ_tests.infra.utils import run_integ_test
from SublimeGHCi.integ_tests.infra.IntegTest import *

class OutputPanelsIntegSpec(unittest.TestCase):
    def test_when_opening_a_cabal_project_with_a_broken_cabal_file_it_should_display_an_error_panel(self):
        test = (IntegTest()
            .using_source_folder('Completions/')
            .add_folder('Completions/BrokenCabalFile')
            .with_file('Completions/BrokenCabalFile/BrokenCabalFile.hs')
            .with_output_panel(lambda panel: panel
                .is_visible()
                .add_result()
                .text()
                .add_result()))

        result = run_integ_test(test)
        self.assertTrue(result[0])
        self.assertTrue('blah' in result[1])