import os
import sys
import time
import traceback
import codecs
import pickle
from threading import Thread

import sublime
import SublimeGHCi.SublimeGHCi as Top


def quit_sublime():
	sublime.run_command('exit')

def write_to_output_file(data):
	output_file = os.environ.get('INTEG_OUTPUT')
	with codecs.open(output_file, 'w+', 'utf-8') as f:
		f.write(data)

def write_exception():
	exc_strs = traceback.format_exception(*sys.exc_info())
	result = ''.join(['EXCEPTION'] + exc_strs)
	write_to_output_file(result)

def after_loaded():
	try:
		while sublime.active_window().active_view() == None:
			time.sleep(0.1)

		result = pickle.loads(test).run(Top.manager, sublime.active_window())
		write_to_output_file('OK\n' + str(result))
		quit_sublime()
	except:
		write_exception()
		quit_sublime()

if os.environ.get('INTEG_TESTS') == '1':
	try:
		test = eval(os.environ.get('INTEG_TEST_SERIALIZED'))

		t = Thread(target=after_loaded)
		t.daemon = True
		t.start()
	except:
		write_exception()
		quit_sublime()
else:
	print('nope')