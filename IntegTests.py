import os

if os.environ.get('INTEG_TESTS') == '1':
	print('yay')
else:
	print('nope')