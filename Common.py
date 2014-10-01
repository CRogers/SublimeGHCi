class Maybe(object):
	def __init__(self, obj):
		self.__obj = obj

	@staticmethod
	def just(value):
		return Maybe(value)

	@staticmethod
	def nothing():
		return Maybe(None)

	def hasValue(self):
		return self.__obj != None

	def value(self):
		return self.__obj

	def bind(self, func):
		if self.hasValue():
			return func(self.value())
		else:
			return Maybe.nothing()