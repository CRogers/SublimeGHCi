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
		self.info_extractor.extract_info_from('', 0)
		self.commands.load_from_string.assert_called_once_with('_hole')

	def test_when_called_calls_inner_commands_load_from_string_with_type_hole_inside_text(self):
		self.info_extractor.extract_info_from('someFunc .  . anotherFunc', 11)
		self.commands.load_from_string.assert_called_once_with('someFunc . _hole . anotherFunc')

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
		type = self.info_extractor.extract_info_from('a .  . b', 4)
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
		type = self.info_extractor.extract_info_from('a .  . b', 4)
		self.assertEqual(type, Fallible.succeed("HList '[Event t Int] -> Moment t (HList '[Event t [Char]])"))