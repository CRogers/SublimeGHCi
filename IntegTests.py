import os, time
import sublime
from threading import Thread
from SublimeGHCi.integ_tests.utils import quit_sublime

def after_loaded():
	while sublime.active_window().active_view() == None:
		time.sleep(0.05)

	output_file = os.environ.get('INTEG_OUTPUT')
	with open(output_file, 'w+') as f:
		f.write(str(getattr(module, func)()))
	quit_sublime()

if os.environ.get('INTEG_TESTS') == '1':
	name = os.environ.get('INTEG_NAME')
	func = os.environ.get('INTEG_FUNC')
	SublimeGHCi = __import__('SublimeGHCi.integ_tests.{}'.format(name))
	module = getattr(SublimeGHCi.integ_tests, name)

	t = Thread(target=after_loaded)
	t.daemon = True
	t.start()
else:
	print('nope')