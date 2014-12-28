import unittest
from unittest.mock import *

from threading import Semaphore
from concurrent.futures import ThreadPoolExecutor

from SublimeGHCi.common.EventHook import *
from SublimeGHCi.common.Fallible import *
from SublimeGHCi.ghci.connection.FailedGhciConnection import *

class NextGhciConnection(object):
	def __init__(self):
		self.load_haskell_file = Mock(return_value=Fallible.succeed('next'))

class LoadingGhciConnection(object):
	def __init__(self):
		self.load_haskell_file = Mock(return_value=Fallible.fail('lel'))
		self.next = EventHook()

class InternalGhciFactory(object):
	def __init__(self):
		self.new_loading_ghci_connection = Mock(return_value=LoadingGhciConnection())

class FailedGhciConnectionSpec(unittest.TestCase):
	def setUp(self):
		self.factory = InternalGhciFactory()
		self.connection = FailedGhciConnection(self.factory, 'failed')

	def test_when_load_haskell_file_is_called_it_should_not_return_the_value_from_the_next_ghci_connection(self):
		executor = ThreadPoolExecutor(max_workers=1)
		future = executor.submit(self.connection.load_haskell_file, 'Foo.hs')
		sema = Semaphore(value=0)
		future.add_done_callback(lambda _: sema.release())
		loading_ghci_connection = self.factory.new_loading_ghci_connection.return_value
		next_ghci_connection = NextGhciConnection()
		loading_ghci_connection.next.fire(next_ghci_connection)
		sema.acquire()
		self.assertTrue(future.done())
		self.assertEqual(future.result(), next_ghci_connection.load_haskell_file.return_value)