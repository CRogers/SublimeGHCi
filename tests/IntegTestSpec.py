import unittest

from SublimeGHCi.integ_tests.infra.IntegTest import IntegTest

class IntegTestSpec(unittest.TestCase):
    def setUp(self):
        self.integ_test = IntegTest()

    def test_when_no_commands_are_added_it_should_return_an_empty_array_when_run(self):
        results = self.integ_test.run(None, None)
        self.assertEqual(results, [])