import unittest

from SublimeGHCi.integ_tests.IntegTest import IntegTest

class Returns():
    def __init__(self, result):
        self._result = result

    def perform(self, results):
        return self._result

class IntegTestSpec(unittest.TestCase):
    def setUp(self):
        self.integ_test = IntegTest()

    def test_when_no_commands_are_run_it_returns_an_empty_list(self):
        results = self.integ_test.run()
        self.assertEqual(results, [])

    def test_when_a_with_file_command_is_called_and_nothing_is_done_with_it_there_are_no_results(self):
        results = self.integ_test.with_file(lambda x: x).run()
        self.assertEqual(results, [])

    def test_when_a_with_file_command_is_called_and_adds_a_result_the_result_is_returned_when_run(self):
        results = (self.integ_test
            .with_file(lambda x: x
                .add_command(Returns(4))
                .add_result())
            .run())
        self.assertEqual(results, [4])

    def test_when_a_with_file_command_adds_two_results_those_two_results_are_returned(self):
        results = (self.integ_test
            .with_file(lambda x: x
                .add_command(Returns(4))
                .add_result()
                .add_command(Returns(5))
                .add_result())
            .run())
        self.assertEqual(results, [4, 5])

    def test_when_two_with_files_each_add_one_results_both_results_are_returned(self):
        results = (self.integ_test
            .with_file(lambda x: x
                .add_command(Returns(1))
                .add_result())
            .with_file(lambda x: x
                .add_command(Returns(2))
                .add_result())
            .run())
        self.assertEqual(results, [1, 2])