import time
import pickle
import subprocess
from threading import Thread

import sublime
from SublimeGHCi.integ_tests.infra.Common import *
import SublimeGHCi.SublimeGHCi as Top

class GitResetter():
	def __init__(self, top_dir):
		self._top_dir = top_dir

	def reset_folders_to_head(self, folders):
		cwd = os.path.join(self._top_dir, 'SublimeGHCi/integ_tests/')
		subprocess.check_call(['git', 'checkout', 'HEAD'] + folders, cwd=cwd)

@save_integ_exceptions
def after_loaded():
	test = eval(os.environ.get('INTEG_TEST_SERIALIZED'))
	top_dir = os.environ.get('INTEG_TEST_DIR')

	while sublime.active_window().active_view() == None:
		time.sleep(0.1)

	sublime.log_commands(True)

	result = pickle.loads(test).run(GitResetter(top_dir), sublime, Top, sublime.active_window())
	write_to_output_file('OK\n' + str(result))
	quit_sublime()

@save_integ_exceptions
def run_integ_tests():
	t = Thread(target=after_loaded)
	t.daemon = True
	t.start()

if os.environ.get('INTEG_TESTS') == '1':
	run_integ_tests()
else:
	print('Not running SublimeGHCi integ tests')