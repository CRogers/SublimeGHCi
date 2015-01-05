import unittest

from SublimeGHCi.integ_tests.infra.utils import run_integ_test
from SublimeGHCi.integ_tests.infra.IntegTest import *

class OutputPanelsIntegSpec(unittest.TestCase):
    def test_when_opening_a_cabal_project_with_a_broken_cabal_file_it_should_display_an_error_panel(self):
        test = (IntegTest()
            .with_folder_file('BrokenCabalFile', 'BrokenCabalFile.hs')
            .with_output_panel(lambda panel: panel
                .is_visible()
                .add_result()
                .text()
                .add_result()))

        result = run_integ_test(test)
        self.assertTrue(result[0])
        self.assertIn('Plain fields are not allowed in between', result[1])

    def test_when_saving_a_file_with_compile_errors_it_should_display_the_error_in_the_error_panel(self):
        test = (IntegTest()
            .with_file('Blank.hs', lambda file: file
                .append_text('cat')
                .save().wait())
            .with_output_panel(lambda panel: panel
                .is_visible()
                .add_result()
                .text()
                .add_result()))

        result = run_integ_test(test)
        self.assertTrue(result[0])
        self.assertIn('Parse error: naked expression at top level', result[1])