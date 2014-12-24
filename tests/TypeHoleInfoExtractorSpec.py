import unittest
from unittest.mock import *

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.ghci.TypeHoleInfoExtractor import *

class GhciCommands(object):
	def __init__(self):
		self.load_from_string = Mock(return_value=Fallible.fail('failed'))

class TypeHoleInfoExtractorSpec(unittest.TestCase):
	def setUp(self):
		self.commands = GhciCommands()
		self.info_extractor = TypeHoleInfoExtractor(self.commands, 'hole')

	def test_when_called_calls_inner_commands_load_from_string_with_type_hole_at_beginning(self):
		self.info_extractor.type_at_range('', 0, 0)
		self.commands.load_from_string.assert_called_once_with('_hole')

	def test_when_called_calls_inner_commands_load_from_string_with_type_hole_inside_text(self):
		self.info_extractor.type_at_range('someFunc . foo . anotherFunc', 11, 3)
		self.commands.load_from_string.assert_called_once_with('someFunc . _hole . anotherFunc')

	def test_when_load_is_unsuccessful_but_has_no_type_hole_errors_it_should_return_fail(self):
		type = self.info_extractor.type_at_range('a .  . b', 4, 0)
		self.assertTrue(type.failed())

	def test_when_load_is_unsuccessful_return_the_type_of_the_hole_simple(self):
		self.commands.load_from_string.return_value = Fallible.fail('''[1 of 1] Compiling X          ( /Users/X.hs, interpreted )

/Users/X.hs:24:17:
    Found hole ‘_hole’ with type: Int
    Relevant bindings include
      hlength :: HList '[] -> Int
        (bound at /Users/X.hs:24:5)
    In the expression: _hole
    In an equation for ‘hlength’: hlength _ = _hole
    In the instance declaration for ‘HLength (HList '[])’
Failed, modules loaded: none.''')
		type = self.info_extractor.type_at_range('a . . b', 4, 0)
		self.assertEqual(type, Fallible.succeed('Int'))

	def test_when_load_is_unsuccessful_return_the_type_of_the_hole_complex(self):
		self.commands.load_from_string.return_value = Fallible.fail('''[1 of 1] Compiling X          ( /Users/X.hs, interpreted )

/Users/X.hs:40:9:
    Found hole ‘_hole’
      with type: HList '[Event t Int]
                 -> Moment t (HList '[Event t [Char]])
    Where: ‘t’ is a rigid type variable bound by
               the type signature for
                 proc1 :: Events t '[Int] -> Moment t (Events t '[String])
               at /Users/X.hs:39:10
    Relevant bindings include
      proc1 :: Events t '[Int] -> Moment t (Events t '[String])
        (bound at /Users/X.hs:40:1)
    In the expression: _
    In an equation for ‘proc1’: proc1 = _
Failed, modules loaded: none.''')
		type = self.info_extractor.type_at_range('a .  . b', 4, 0)
		self.assertEqual(type, Fallible.succeed("HList '[Event t Int] -> Moment t (HList '[Event t [Char]])"))

	def test_when_load_is_unsucessful_because_the_hole_was_applied_to_a_function_that_needs_two_arguments_to_typecheck_it_should_add_an_extra_dummy_hole(self):
		self.commands.load_from_string.side_effect = [Fallible.fail('''
<interactive>:3:1:
    Couldn't match expected type ‘Int’ with actual type ‘b0 -> a0’
    Probable cause: ‘const’ is applied to too few arguments
    In the expression: const _ :: Int
    In an equation for ‘it’: it = const _ :: Int'''), Fallible.fail('''Generic fail''')]
		self.info_extractor.type_at_range('const x :: Int', 6, 1)
		self.commands.load_from_string.assert_called_with('const _hole _dummyhole :: Int')

	def test_when_load_is_unsucessful_because_the_hole_was_applied_to_a_function_that_needs_two_arguments_to_typecheck_it_should_return_the_type_from_the_attempt_with_the_dummy_hole(self):
		self.commands.load_from_string.side_effect = [Fallible.fail('''
<interactive>:3:1:
    Couldn't match expected type ‘Int’ with actual type ‘b0 -> a0’
    Probable cause: ‘const’ is applied to too few arguments
    In the expression: const _ :: Int
    In an equation for ‘it’: it = const _ :: Int'''),
		Fallible.fail('''
<interactive>:5:7:
    Found hole ‘_hole’ with type: Int
    Relevant bindings include it :: Int (bound at <interactive>:5:1)
    In the first argument of ‘const’, namely ‘_hole’
    In the expression: const _hole _dummyhole :: Int
    In an equation for ‘it’: it = const _hole _dummyhole :: Int

<interactive>:5:13:
    Found hole ‘_dummyhole’ with type: b0
    Where: ‘b0’ is an ambiguous type variable
    Relevant bindings include it :: Int (bound at <interactive>:5:1)
    In the second argument of ‘const’, namely ‘_dummyhole’
    In the expression: const _hole _dummyhole :: Int
    In an equation for ‘it’: it = const _hole _dummyhole :: Int''')]
		type = self.info_extractor.type_at_range('const x :: Int', 6, 1)
		self.assertEqual(type, Fallible.succeed('Int'))




