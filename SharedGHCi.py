class SharedGHCiCommand(object):
	def __init__(self, commands):
		self.__commands = commands
		self.__counter = 0

	def open(self):
		self.__counter += 1

	def close(self):
		self.__counter -= 1
		if self.__counter == 0:
			self.__commands.close()

	def completions(self, prefix):
		return self.__commands.completions(prefix)

	def type_of(self, expr):
		return self.__commands.type_of(expr)

	def kind_of(self, expr):
		return self.__commands.kind_of(expr)

	def type_or_kind_of(self, expr):
		return self.__commands.type_or_kind_of(expr)

	def load_haskell_file(self, file_name):
		return self.__commands.load_haskell_file(file_name)