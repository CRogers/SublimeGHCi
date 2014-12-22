import os, os.path, subprocess, tempfile

default_path = '/Applications/Sublime Text.app/Contents/MacOS/Sublime Text'

def wait_until_sublime_closes(popen):
	while not popen.poll():
		try:
			popen.wait(0.1)
			break
		except subprocess.TimeoutExpired:
			pass

def run_sublime(env, *paths_to_open):
	path = os.environ.get('SUBLIME_PATH', default_path)
	p = subprocess.Popen([path] + list(paths_to_open), env=env)
	wait_until_sublime_closes(p)

def run_integ_test(func, *files):
	env = os.environ.copy()
	env['INTEG_TESTS'] = '1'
	env['INTEG_NAME'] = func.__module__
	env['INTEG_FUNC'] = func.__name__
	tfname = None
	with tempfile.NamedTemporaryFile(delete=False) as tf:
		tfname = tf.name
		env['INTEG_OUTPUT'] = tf.name
		tf.write(b'EXCEPTION\nINFRA ERROR')
	
	run_sublime(env, *files)

	lines = None
	with open(tfname, 'r') as tf:
		lines = tf.readlines()
	os.unlink(tfname)
	bulk = '\n'.join(lines[1:])
	if lines[0].startswith('EXCEPTION'):
		raise Exception(bulk)
	return bulk