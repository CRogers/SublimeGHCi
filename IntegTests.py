import os
import os.path
import sys
import time
import traceback
import codecs
import pickle
import subprocess
from threading import Thread

import sublime
import SublimeGHCi.SublimeGHCi as Top

class GitResetter():
	def __init__(self, top_dir):
		self._top_dir = top_dir

	def reset_folders_to_head(self, folders):
		cwd = os.path.join(self._top_dir, 'SublimeGHCi/integ_tests/')
		subprocess.check_call(['git', 'checkout', 'HEAD'] + folders, cwd=cwd)

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

		result = pickle.loads(test).run(GitResetter(top_dir), sublime, Top.manager, sublime.active_window())
		write_to_output_file('OK\n' + str(result))
		quit_sublime()
	except:
		write_exception()
		quit_sublime()

if os.environ.get('INTEG_TESTS') == '1':
	try:
		sublime.log_commands(True)
		test = eval(os.environ.get('INTEG_TEST_SERIALIZED'))
		top_dir = os.environ.get('INTEG_TEST_DIR')

		t = Thread(target=after_loaded)
		t.daemon = True
		t.start()
	except:
		write_exception()
		quit_sublime()
else:
	print('nope')