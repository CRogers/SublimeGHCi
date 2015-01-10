import sublime
import codecs
import os
import traceback
import sys

def integ_tests_are_running():
    return os.environ.get('INTEG_TESTS') == '1'

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

def record_integ_exception():
    if integ_tests_are_running():
        write_exception()
        quit_sublime()
    else:
        exc_info = sys.exc_info()
        raise exc_info[0](exc_info[1]).with_traceback(exc_info[2])

def save_integ_exceptions(func):
    def ret(*args):
        try:
            return func(*args)
        except:
            record_integ_exception()
    return ret