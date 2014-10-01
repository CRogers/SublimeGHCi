import re

def get_last_part(sig):
	return re.match(r'([A-Z].*?\.)*(.*)$', sig).group(2)

def get_info_part(str):
	return re.sub(r'^.* :: (.*?)$', r'\1', str)

def is_not_defined(str):
	return re.search(r'Not in scope', str) != None

class GHCiCommands(object):
	def __init__(self, ghci_connection):
		self.__ghci = ghci_connection

	def completions(self, prefix = ''):
		msg = ':complete repl 1000000 "{}"'.format(prefix)
		lines = self.__ghci.message(msg).split('\n')[1:]
		completions = [re.sub(r'"(.*)"', r'\1', line) for line in lines if line != '']
		return completions

	def __expr_command(self, command, expr):
		msg = ':{} ({})'.format(command, expr)
		response = self.__ghci.message(msg)
		if is_not_defined(response):
			return ''
		return get_info_part(response)

	def get_type(self, expr):
		return self.__expr_command('t', expr)

	def get_kind(self, expr):
		return self.__expr_command('k', expr)

	def get_type_or_kind(self, sig):
		last_part = get_last_part(sig)
		type_ = self.get_type(sig)
		if type_ == '':
			return self.get_kind(sig)
		return type_

	def load_haskell_file(self, file_name):
		msg = ':load "{}"'.format(file_name)
		return self.__ghci.message(msg)