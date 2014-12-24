import os, os.path, time, subprocess, tempfile

default_path = '/Applications/Sublime Text.app/Contents/MacOS/Sublime Text'

def wait_until_complete(tfname):
	while not os.path.exists(tfname):
		print('waiting')
		time.sleep(1)

def run_sublime(env, tfname, *paths_to_open):
	path = os.environ.get('SUBLIME_PATH', default_path)
	print('starting subprocess')
	subprocess.call([path] + list(paths_to_open), env=env, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	wait_until_complete(tfname)

def run_integ_test(func, *files):
	env = os.environ.copy()
	env['INTEG_TESTS'] = '1'
	env['INTEG_NAME'] = func.__module__
	env['INTEG_FUNC'] = func.__name__
	tfname = None
	with tempfile.NamedTemporaryFile(delete=False) as tf:
		tfname = tf.name
	os.unlink(tfname)
	env['INTEG_OUTPUT'] = tfname
	
	run_sublime(env, tfname, *files)

	if not os.path.exists(tfname):
		raise Exception('Infra error')

	lines = None
	with open(tfname, 'r') as tf:
		lines = tf.readlines()
	os.unlink(tfname)
	bulk = ''.join(lines[1:])
	if lines[0].startswith('EXCEPTION'):
		raise Exception(bulk)
	return bulk