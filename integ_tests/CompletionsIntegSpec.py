import unittest
import os.path

from SublimeGHCi.integ_tests.infra.utils import run_integ_test
from SublimeGHCi.integ_tests.infra.IntegTest import *


def top_level_two_hole(file_test):
	return (file_test
		.wait()
		.append_text('a :: Foo\n')
		.append_text('a = takes ')
		.complete('Foo')
		.add_result())

def top_level_completion_with(prefix):
	return (lambda file: file
		.wait()
		.append_text('a = ')
		.complete(prefix)
		.add_result())

def completion(expr, type):
	return ('{}\t{}'.format(expr, type), expr)

def with_tick(expr, type):
	fst, snd = completion(expr, type)
	return (fst + '\t\u2713', snd)

def completion_test():
	return IntegTest()

class CompletionsIntegSpec(unittest.TestCase):
	def test_no_completions(self):
		test = (completion_test()
			.with_file('NoCompletions.hs', top_level_completion_with('f')))

		result = run_integ_test(test)
		self.assertEqual(result, [[]])

	def test_one_completion(self):
		test = (completion_test()
			.with_file('OneCompletion.hs', top_level_completion_with('f')))

		result = run_integ_test(test)
		self.assertEqual(result, [[with_tick('foo', 'Foo')]])

	def test_should_suggest_only_module_prefixed_completions_after_dot(self):
		test = (completion_test()
			.add_folder('MultipleModules')
			.with_file('MultipleModules/SecondModule.hs', top_level_completion_with('F')))

		result = run_integ_test(test)
		self.assertEqual(result, [[completion('FirstModule.bar','FirstModule.Bar')]])

	def test_mutliple_modules(self):
		test = (completion_test()
			.add_folder('MultipleModules')
			.with_file('MultipleModules/SecondModule.hs', top_level_completion_with('b')))

		result = run_integ_test(test)
		self.assertEqual(result, [[completion('bar', 'FirstModule.Bar')]])

	def test_should_suggest_an_expression_which_fits_the_type_at_that_position_over_one_that_does_not(self):
		test = (completion_test()
			.with_file('TypeHole.hs', lambda file: file
				.append_text('a = takesFoo ')
				.complete('f')
				.add_result()))

		result = run_integ_test(test)
		self.assertEqual(result, [[with_tick('fooForReal', 'Foo'), completion('fooFake','FooFake')]])

	def test_should_put_a_tick_next_to_an_expression_when_it_fits_were_there_to_be_a_single_further_argument_to_the_function(self):
		test = (completion_test()
			.with_file('TypeHole2.hs', top_level_two_hole))

		result = run_integ_test(test)
		self.assertEqual(result, [[with_tick('Foo', 'Foo')]])

	def test_should_put_a_tick_next_to_an_expression_when_it_fits_were_there_to_be_two_further_arguments_to_the_function(self):
		test = (completion_test()
			.with_file('TypeHole3.hs', top_level_two_hole))

		result = run_integ_test(test)
		self.assertEqual(result, [[with_tick('Foo', 'Foo')]])

	def test_when_loading_a_cabal_library_with_compile_errors_completions_work_again_after_the_errors_have_been_fixed(self):
		test = (completion_test()
			.add_folder('DoesNotCompile')
			.with_file('DoesNotCompile/DoesNotCompile.hs', lambda file: file
				.append_text('3\n')
				.save()
				.append_text('a = ')
				.complete('Bar')
				.add_result()))

		result = run_integ_test(test)
		self.assertEqual(result, [[with_tick('Bar', 'Bar')]])

	def test_when_loading_a_cabal_library_with_a_broken_cabal_file_it_should_work_if_the_cabal_file_is_fixed(self):
		haskell_file = 'BrokenCabalFile/BrokenCabalFile.hs'
		cabal_file = 'BrokenCabalFile/BrokenCabalFile.cabal'

		test = (completion_test()
			.with_file(haskell_file, lambda file: file
				.complete('Bar')
				.add_result())
			.with_file(cabal_file, lambda file: file
				.delete_range(0, 6)
				.save())
			.with_file(haskell_file, lambda file: file
				.delete_left_from_end(3)
				.append_text('3')
				.save()
				.delete_left_from_end(1)
				.complete('Bar')
				.add_result()))

		result = run_integ_test(test)
		self.assertEqual(result, [
			[],
			[with_tick('Bar', 'Bar')]
		])

	def test_when_a_cabal_project_depends_on_a_library_it_should_be_able_to_complete_from_that_library(self):
		test = (completion_test()
			.add_folder('BuildDepends')
			.with_file('BuildDepends/BuildDepends.hs', top_level_completion_with('empty')))

		result = run_integ_test(test)
		self.assertEqual(result, [[with_tick('empty', 'Map k a')]])

	def test_when_a_cabal_project_has_multiple_source_dirs_we_can_load_code_across_them(self):
		test = (completion_test()
			.add_folder('MultipleSourceDirs')
			.with_file('MultipleSourceDirs/src2/Two.hs', top_level_completion_with('Foo')))

		result = run_integ_test(test)
		self.assertEqual(result, [[with_tick('Foo', 'Foo')]])