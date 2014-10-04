import re
from SublimeGHCi.Common import *

def get_last_part(sig):
	return re.match(r'([A-Z].*?\.)*(.*)$', sig).group(2)

def get_info_part(str):
	return re.sub(r'^.* :: (.*?)$', r'\1', str)

def is_defined(str):
	return re.search(r'Not in scope', str) == None

def load_succeeded(response):
	return re.search(r'Failed, modules loaded:', response) == None

class GHCiCommands(object):
	def __init__(self, ghci_connection):
		self.__ghci = ghci_connection

	def connection(self):
		return self.__ghci

	def completions(self, prefix = ''):
		msg = ':complete repl 1000000 "{}"'.format(prefix)
		lines = self.__ghci.message(msg).split('\n')[1:]
		completions = [re.sub(r'"(.*)"', r'\1', line) for line in lines if line != '']
		return Fallible.succeed(completions)

	def __expr_command(self, command, expr):
		msg = ':{} ({})'.format(command, expr)
		response = self.__ghci.message(msg)
		return (Fallible
			.from_bool(is_defined, response)
			.map(get_info_part))

	def type_of(self, expr):
		return self.__expr_command('t', expr)

	def kind_of(self, expr):
		return self.__expr_command('k', expr)

	def type_or_kind_of(self, sig):
		last_part = get_last_part(sig) 
		return (self
			.type_of(sig)
			.or_else(lambda _: self.kind_of(sig)))

	def load_haskell_file(self, file_name):
		msg = ':load "{}"'.format(file_name)
		response = self.__ghci.message(msg)
		return Fallible.from_bool(load_succeeded, response)