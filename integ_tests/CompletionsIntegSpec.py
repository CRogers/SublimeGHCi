import unittest

from SublimeGHCi.integ_tests.utils import run_integ_test
from SublimeGHCi.integ_tests.infra.IntegTest import *

def top_level_two_hole(file):
	return (IntegTest()
		.open(file)
			.append_text('a :: Foo\n')
			.append_text('a = takes ')
			.complete('Foo')
			.add_result())

def top_level_completion_with(view_open_test, prefix):
	return (view_open_test
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
		test = (IntegTest()
			.open_file('Completions/NoCompletions.hs'))

		result = run_integ_test(top_level_completion_with(test, 'f'))
		self.assertEqual(result, [[]])

	def test_one_completion(self):
		test = (IntegTest()
			.open_file('Completions/OneCompletions.hs'))

		result = run_integ_test(top_level_completion_with(test, 'f'))
		self.assertEqual(result, [[with_tick('foo', 'Foo')]])

	def test_should_suggest_only_module_prefixed_completions_after_dot(self):
		test = (IntegTest()
			.add_folder('Completions/MultipleModules')
			.open_file('Completions/MultipleModules/SecondModule.hs'))

		result = run_integ_test(top_level_completion_with(test, 'F'))
		self.assertEqual(result, [[completion('FirstModule.bar','FirstModule.Bar')]])

	def test_mutliple_modules(self):
		test = (IntegTest()
			.add_folder('Completions/MultipleModules')
			.open_file('Completions/MultipleModules/SecondModule.hs'))

		result = run_integ_test(top_level_completion_with(test, 'b'))
		self.assertEqual(result, [[completion('bar', 'FirstModule.Bar')]])

	def test_should_suggest_an_expression_which_fits_the_type_at_that_position_over_one_that_does_not(self):
		test = (IntegTest()
			.open('Completions/TypeHole.hs')
				.append_text('a = takesFoo ')
				.complete('f')
				.add_result())

		result = run_integ_test(test)
		self.assertEqual(result, [[with_tick('fooForReal', 'Foo'), completion('fooFake','FooFake')]])

	def test_should_put_a_tick_next_to_an_expression_when_it_fits_were_there_to_be_a_single_further_argument_to_the_function(self):
		result = run_integ_test(top_level_two_hole('Completions/TypeHole2.hs'))
		self.assertEqual(result, [[with_tick('Foo', 'Foo')]])

	def test_should_put_a_tick_next_to_an_expression_when_it_fits_were_there_to_be_two_further_arguments_to_the_function(self):
		result = run_integ_test(top_level_two_hole('Completions/TypeHole3.hs'))
		self.assertEqual(result, [[with_tick('Foo', 'Foo')]])

	def test_when_loading_a_cabal_library_with_compile_errors_completions_work_again_after_the_errors_have_been_fixed(self):
		test = (IntegTest()
			.add_folder('Completions/DoesNotCompile')
			.open_file('Completions/DoesNotCompile/DoesNotCompile.hs')
				.append_text('3\n')
				.save()
				.append_text('a = ')
				.complete('Bar')
				.add_result())

		result = run_integ_test(test)
		self.assertEqual(result, [[with_tick('Bar', 'Bar')]])

	@unittest.skip('not finished')
	def test_when_loading_a_cabal_library_with_a_broken_cabal_file_it_should_work_if_the_cabal_file_is_fixed(self):
		test = (IntegTest()
			.open_file('Completions/BrokenCabalFile/BrokenCabalFile.hs')
				.append_text('cat')
				.complete('yay')
				.add_result()
				.back()
			.open_file('Completions/BrokenCabalFile/broken-cabal-file.cabal')
				.insert_text('yay')
				.save()
				.close()
			.open_file('Completions/BrokenCabalFile/BrokenCabalFile.hs')
				.delete_left(3)
				.complete('yay')
				.add_result())

		result = run_integ_test(test)
		self.assertEqual(result, [
			[],
			[with_tick('Foo', 'Foo')]
		])