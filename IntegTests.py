import os

if os.environ.get('INTEG_TESTS') == '1':
	name = os.environ.get('INTEG_NAME')
	func = os.environ.get('INTEG_FUNC')
	SublimeGHCi = __import__('SublimeGHCi.integ_tests.{}'.format(name))
	module = getattr(SublimeGHCi.integ_tests, name)
	getattr(module, func)()
else:
	print('nope')