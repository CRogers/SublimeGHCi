import sublime

class Fallible(object):
	def __init__(self, succeeded, value):
		self.__succeeded = succeeded
		self.__value = value

	@staticmethod
	def fail(value):
		return Fallible(False, value)

	@staticmethod
	def succeed(value):
		return Fallible(True, value)

	@staticmethod
	def from_bool(bool_func, value):
		return Fallible(bool_func(value), value)

	def successful(self):
		return self.__succeeded

	def failed(self):
		return not self.successful()

	def value(self):
		return self.__value

	def switch(self, succeed, fail):
		if self.successful():
			return succeed(self.value())
		else:
			return fail(self.value())

	def bind(self, func):
		return self.switch(func, Fallible.fail)

	def map(self, func):
		return self.bind(lambda x: Fallible.succeed(func(x)))

	def or_else(self, func):
		return self.switch(Fallible.succeed, func)

	def mapFail(self, func):
		return self.or_else(lambda x: Fallible.fail(func(x)))

def find_open_file(file_name):
	for window in sublime.windows():
		for view in window.views():
			if view.file_name() == file_name:
				return view