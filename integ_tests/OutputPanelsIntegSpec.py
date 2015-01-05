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

        [visible, error] = run_integ_test(test)
        self.assertTrue(visible)
        self.assertIn('Plain fields are not allowed in between', error)

    def test_when_saving_a_file_with_compile_errors_it_should_display_the_error_in_the_error_panel(self):
        test = (IntegTest()
            .with_file('Blank.hs', lambda file: file
                .append_text('cat')
                .save())
            .with_output_panel(lambda panel: panel
                .is_visible()
                .add_result()
                .text()
                .add_result()))

        [visible, error] = run_integ_test(test)
        self.assertTrue(visible)
        self.assertIn('Parse error: naked expression at top level', error)

    def test_when_saving_a_file_that_had_saved_compile_errors_that_were_then_fixed_the_error_panel_should_not_be_visible(self):
        test = (IntegTest()
            .with_file('Blank.hs', lambda file: file
                .append_text('cat')
                .save()
                .delete_left_from_end(3)
                .save())
            .with_output_panel(lambda panel: panel
                .is_visible()
                .add_result()))

        [visible] = run_integ_test(test)
        self.assertFalse(visible)