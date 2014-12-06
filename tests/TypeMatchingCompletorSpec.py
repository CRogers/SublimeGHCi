import unittest
from unittest.mock import *

from SublimeGHCi.completions.TypeMatchingCompletor import *

class TypeMatchingCompletorSpec(unittest.TestCase):
	def setUp(self):
		self.type_matching_completor = TypeMatchingCompletor()