import os, os.path, time, subprocess, tempfile, codecs, pickle

default_path = '/Applications/Sublime Text.app/Contents/MacOS/Sublime Text'

def wait_until_complete(tfname):
	while not os.path.exists(tfname):
		time.sleep(0.1)

def run_sublime(env, tfname, *paths_to_open):
	path = os.environ.get('SUBLIME_PATH', default_path)
	paths_to_open = map(lambda path: 'SublimeGHCi/integ_tests/' + path, paths_to_open)
	subprocess.call([path] + list(paths_to_open), env=env, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	wait_until_complete(tfname)

def run_integ_test(test):
	env = os.environ.copy()
	env['INTEG_TESTS'] = '1'
	env['INTEG_TEST_SERIALIZED'] = str(pickle.dumps(test, 3))
	tfname = None
	with tempfile.NamedTemporaryFile(delete=False) as tf:
		tfname = tf.name
	os.unlink(tfname)
	env['INTEG_OUTPUT'] = tfname

	run_sublime(env, tfname)

	if not os.path.exists(tfname):
		raise Exception('Infra error')

	lines = None
	with codecs.open(tfname, 'r', 'utf-8') as tf:
		lines = tf.readlines()
	os.unlink(tfname)
	bulk = ''.join(lines[1:])
	if lines[0].startswith('EXCEPTION'):
		raise Exception(bulk)
	return eval(bulk)