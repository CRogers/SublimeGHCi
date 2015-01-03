import unittest

from SublimeGHCi.integ_tests.utils import run_integ_test
from SublimeGHCi.integ_tests.infra.IntegTest import *

def top_level_two_hole():
	return (IntegTest()
		.wait()
		.append_text('a :: Foo\n')
		.append_text('a = takes ')
		.complete('Foo')
		.add_result())

def top_level_completion_with(prefix):
	return (IntegTest()
		.wait()
		.append_text('a = ')
		.complete(prefix)
		.add_result())

def completion(expr, type):
	return ('{}\t{}'.format(expr, type), expr)

def with_tick(expr, type):
	fst, snd = completion(expr, type)
	return (fst + '\t\u2713', snd)

class CompletionsIntegSpec(unittest.TestCase):
	def test_no_completions(self):
		result = run_integ_test(['Completions/NoCompletions.hs'], top_level_completion_with('f'))
		self.assertEqual(result, [[]])

	def test_one_completion(self):
		result = run_integ_test(['Completions/OneCompletion.hs'], top_level_completion_with('f'))
		self.assertEqual(result, [[with_tick('foo', 'Foo')]])

	def test_should_suggest_only_module_prefixed_completions_after_dot(self):
		result = run_integ_test(['Completions/MultipleModules', 'Completions/MultipleModules/SecondModule.hs'], top_level_completion_with('F'))
		self.assertEqual(result, [[completion('FirstModule.bar','FirstModule.Bar')]])

	def test_mutliple_modules(self):
		result = run_integ_test(['Completions/MultipleModules', 'Completions/MultipleModules/SecondModule.hs'], top_level_completion_with('b'))
		self.assertEqual(result, [[completion('bar', 'FirstModule.Bar')]])

	def test_should_suggest_an_expression_which_fits_the_type_at_that_position_over_one_that_does_not(self):
		test = (IntegTest()
			.wait()
			.append_text('a = takesFoo ')
			.complete('f')
			.add_result())
		result = run_integ_test(['Completions/TypeHole.hs'], test)
		self.assertEqual(result, [[with_tick('fooForReal', 'Foo'), completion('fooFake','FooFake')]])

	def test_should_put_a_tick_next_to_an_expression_when_it_fits_were_there_to_be_a_single_further_argument_to_the_function(self):
		result = run_integ_test(['Completions/TypeHole2.hs'], top_level_two_hole())
		self.assertEqual(result, [[with_tick('Foo', 'Foo')]])

	def test_should_put_a_tick_next_to_an_expression_when_it_fits_were_there_to_be_two_further_arguments_to_the_function(self):
		result = run_integ_test(['Completions/TypeHole3.hs'], top_level_two_hole())
		self.assertEqual(result, [[with_tick('Foo', 'Foo')]])

	def test_when_loading_a_cabal_library_with_compile_errors_completions_work_again_after_the_errors_have_been_fixed(self):
		test = (IntegTest()
			.add_folder('Completions/DoesNotCompile')
			.with_file('Completions/DoesNotCompile/DoesNotCompile.hs')
			.append_text('3\n')
			.save()
			.append_text('a = ')
			.complete('Bar')
			.add_result())
		result = run_integ_test(['Completions/DoesNotCompile', 'Completions/DoesNotCompile/DoesNotCompile.hs'], test)
		self.assertEqual(result, [[with_tick('Bar', 'Bar')]])

	@unittest.skip('not finished')
	def test_when_loading_a_cabal_library_with_a_broken_cabal_file_it_should_work_if_the_cabal_file_is_fixed(self):
		test = (IntegTest()
			.with_file('Completions/BrokenCabalFile/BrokenCabalFile.hs', lambda file: file
				.append_text('cat')
				.complete('yay')
				.add_result())
			.with_file('Completions/BrokenCabalFile/broken-cabal-file.cabal', lambda file: file
				.insert_text('yay')
				.save()
				.close())
			.with_file('Completions/BrokenCabalFile/BrokenCabalFile.hs', lambda file: file
				.delete_left(3)
				.complete('yay')
				.add_result()))
		result = run_integ_test(test)
		self.assertEqual(result, [
			[],
			[with_tick('Foo', 'Foo')]
		])