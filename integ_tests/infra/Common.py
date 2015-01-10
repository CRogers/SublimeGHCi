import sublime
import codecs
import os
import traceback
import sys

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

def save_integ_exceptions(func):
    def ret(*args):
        try:
            return func(*args)
        except:
            write_exception()
            quit_sublime()
    return ret