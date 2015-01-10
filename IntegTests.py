import time
import pickle
import subprocess
from threading import Thread

import sublime
from SublimeGHCi.integ_tests.infra.Common import *
import SublimeGHCi.SublimeGHCi as Top

def reset_folders_to_head(top_dir):
    haskell = os.path.join(top_dir, 'SublimeGHCi/integ_tests/Haskell')
    subprocess.check_call(['git', 'checkout', 'HEAD', haskell], cwd=haskell)

@save_integ_exceptions
def after_loaded():
    test = eval(os.environ.get('INTEG_TEST_SERIALIZED'))
    top_dir = os.environ.get('INTEG_TEST_DIR')

    while sublime.active_window().active_view() == None:
        time.sleep(0.1)

    result = pickle.loads(test).run(sublime, Top, sublime.active_window())
    reset_folders_to_head(top_dir)

    write_to_output_file('OK\n' + str(result))
    quit_sublime()

@save_integ_exceptions
def run_integ_tests():
    t = Thread(target=after_loaded)
    t.daemon = True
    t.start()

if integ_tests_are_running():
    run_integ_tests()
else:
    print('Not running SublimeGHCi integ tests')