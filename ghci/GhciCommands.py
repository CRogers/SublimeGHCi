import re

from SublimeGHCi.common.Fallible import *
from SublimeGHCi.common.Regexes import *

def get_info_part(str):
	type_with_breaks = re.sub(r'^(?:\n|.)*::((?:.|\n)*?)$', r'\1', str)
	return strip_whitespace_on_leading_lines(type_with_breaks)

ambiguous_regex = r'Ambiguous occurrence(?:\n|.)*?either ‘(.*?)’(?:\n|.)*?or ‘(.*?)’'

def is_ambiguous(str):
	match = re.search(ambiguous_regex, str)
	if match != None:
		return 'Ambiguous: {} or {}'.format(match.group(1), match.group(2))
	return str

def no_error_occurred(str):
	return re.match(r'\n?<interactive>', str) == None

def is_defined(str):
	return re.search(r'Not in scope', str) == None

def load_succeeded(response):
	return re.search(r'Failed, modules loaded:', response) == None

class GhciCommands(object):
	def __init__(self, ghci_connection):
		self.__ghci = ghci_connection

	def close(self):
		self.__ghci.terminate()

	def loaded(self):
		return self.__ghci.loaded()

	def completions(self, prefix = ''):
		msg = ':complete repl 1000000 "{}"'.format(prefix)
		lines = self.__ghci.message(msg).split('\n')[1:]
		completions = {re.sub(r'"(.*)"', r'\1', line) for line in lines if line != ''}
		return Fallible.succeed(list(completions))

	def __expr_command(self, command, expr):
		msg = ':{} ({})'.format(command, expr)
		response = self.__ghci.message(msg)
		return (Fallible
			.from_bool(no_error_occurred, response)
			.map_fail(is_ambiguous)
			.map(get_info_part))

	def type_of(self, expr):
		return (self.__expr_command('t', expr))

	def kind_of(self, expr):
		return self.__expr_command('k', expr)

	def load_haskell_file(self, file_name):
		msg = ':load "{}"'.format(file_name)
		response = self.__ghci.message(msg)
		return Fallible.from_bool(load_succeeded, response)

	def reload(self):
		response = self.__ghci.message(':r')
		return Fallible.from_bool(load_succeeded, response)

	def run_expr(self, expr):
		response = self.__ghci.message(expr)
		return Fallible.from_bool(is_defined, response)
