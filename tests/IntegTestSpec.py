import unittest
from unittest.mock import *

from SublimeGHCi.integ_tests.infra.IntegTest import IntegTest


class Returns():
    def __init__(self, result):
        self._result = result

    def perform(self, context):
        return self._result

class MockCommand():
    def __init__(self):
        self.perform = Mock()
        self.undo = Mock()

class Manager():
    def loaded(self, view):
        return True

class View():
    def __init__(self):
        self.run_command = Mock()
        self.is_loading = Mock(return_value=False)

class Window():
    def __init__(self):
        self.open_file = Mock(return_value=View())
        self.run_command = Mock()

class Sublime():
    pass

class IntegTestSpec(unittest.TestCase):
    def setUp(self):
        self.sublime = Sublime()
        self.manager = Manager()
        self.window = Window()
        self.runargs = (self.sublime, self.manager, self.window)
        self.integ_test = IntegTest()

    def test_when_no_commands_are_run_it_returns_an_empty_list(self):
        results = self.integ_test.run(*self.runargs)
        self.assertEqual(results, [])

    def test_when_a_with_file_command_is_called_and_nothing_is_done_with_it_there_are_no_results(self):
        results = self.integ_test.with_file('a', lambda x: x).run(*self.runargs)
        self.assertEqual(results, [])

    def test_when_a_with_file_command_is_called_and_adds_a_result_the_result_is_returned_when_run(self):
        results = (self.integ_test
            .with_file('a', lambda x: x
                .add_command(Returns(4))
                .add_result())
            .run(*self.runargs))
        self.assertEqual(results, [4])

    def test_when_a_with_file_command_adds_two_results_those_two_results_are_returned(self):
        results = (self.integ_test
            .with_file('a', lambda x: x
                .add_command(Returns(4))
                .add_result()
                .add_command(Returns(5))
                .add_result())
            .run(*self.runargs))
        self.assertEqual(results, [4, 5])

    def test_when_two_with_files_each_add_one_results_both_results_are_returned(self):
        results = (self.integ_test
            .with_file('a', lambda x: x
                .add_command(Returns(1))
                .add_result())
            .with_file('a', lambda x: x
                .add_command(Returns(2))
                .add_result())
            .run(*self.runargs))
        self.assertEqual(results, [1, 2])

    def test_when_a_single_command_is_added_its_perform_method_is_called(self):
        command = MockCommand()
        self.integ_test.add_command(command).run(*self.runargs)
        self.assertEqual(command.perform.call_count, 1)

    def test_when_a_single_command_is_added_its_perform_method_is_not_called_until_run_is_called(self):
        command = MockCommand()
        self.integ_test.add_command(command)
        self.assertFalse(command.perform.called)

    def test_when_two_commands_are_added_their_performs_are_called_in_order(self):
        call_order = []
        def make_command(num):
            command = MockCommand()
            command.perform.side_effect = lambda _: call_order.append(num)
            return command
        command1 = make_command(1)
        command2 = make_command(2)
        self.integ_test.add_command(command1).add_command(command2).run(*self.runargs)
        self.assertEqual(call_order, [1, 2])

    def test_when_a_single_command_is_added_its_undo_method_is_called_when_run(self):
        command = MockCommand()
        self.integ_test.add_command(command).run(*self.runargs)
        self.assertEqual(command.undo.call_count, 1)

    def test_when_a_single_command_is_add_its_undo_method_is_not_called_if_run_isnt_called(self):
        command = MockCommand()
        self.integ_test.add_command(command)
        self.assertFalse(command.undo.called)

    def test_when_two_commands_are_added_their_undo_methods_are_called_in_reversed_order(self):
        call_order = []
        def make_command(num):
            command = MockCommand()
            command.undo.side_effect = lambda _: call_order.append(num)
            return command
        command1 = make_command(1)
        command2 = make_command(2)
        self.integ_test.add_command(command1).add_command(command2).run(*self.runargs)
        self.assertEqual(call_order, [2, 1])

    def test_when_a_command_is_added_its_perform_method_is_called_before_its_undo_method(self):
        call_order = []
        command = MockCommand()
        command.perform.side_effect = lambda _: call_order.append('perform')
        command.undo.side_effect = lambda _: call_order.append('undo')
        self.integ_test.add_command(command).run(*self.runargs)
        self.assertEqual(call_order, ['perform', 'undo'])

    def test_when_a_command_is_added_its_perform_method_should_be_given_a_context_object_with_a_manager_a_window_and_sublime(self):
        command = MockCommand()
        self.integ_test.add_command(command).run(*self.runargs)
        context = command.perform.call_args[0][0]
        self.assertEqual(context.manager(), self.manager)
        self.assertEqual(context.window(), self.window)
        self.assertEqual(context.sublime(), self.sublime)

    def test_when_with_file_is_called_the_file_test_performs_get_a_context_with_a_manager_window_sublime_and_view_from_window_dot_open_file(self):
        command = MockCommand()
        (self.integ_test
            .with_file('a', lambda x: x
                .add_command(command))
            .run(*self.runargs))
        context = command.perform.call_args[0][0]
        self.assertEqual(context.manager(), self.manager)
        self.assertEqual(context.window(), self.window)
        self.assertEqual(context.sublime(), self.sublime)
        self.assertEqual(context.view(), self.window.open_file.return_value)