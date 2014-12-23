import os, sys, time, signal, traceback
import sublime
from threading import Thread

def quit_sublime():
	os.kill(os.getppid(), signal.SIGTERM)

def write_to_output_file(data):
	output_file = os.environ.get('INTEG_OUTPUT')
	with open(output_file, 'w+') as f:
		f.write(data)

def write_exception():
	exc_strs = traceback.format_exception(*sys.exc_info())
	result = ''.join(['EXCEPTION'] + exc_strs)
	write_to_output_file(result)

def after_loaded():
	try:
		while sublime.active_window().active_view() == None:
			time.sleep(0.05)

		result = getattr(module, func)()
		write_to_output_file('OK\n' + str(result))
		quit_sublime()
	except:
		write_exception()
		quit_sublime()

if os.environ.get('INTEG_TESTS') == '1':
	try:
		name = os.environ.get('INTEG_NAME')
		func = os.environ.get('INTEG_FUNC')
		SublimeGHCi = __import__('SublimeGHCi.integ_tests.{}'.format(name))
		module = getattr(SublimeGHCi.integ_tests, name)

		t = Thread(target=after_loaded)
		t.daemon = True
		t.start()
	except e:
		write_exception()
		quit_sublime()
else:
	print('nope')