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
	p = subprocess.Popen([path] + list(paths_to_open), env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	wait_until_sublime_closes(p)

def run_integ_test(func, *files):
	env = os.environ.copy()
	env['INTEG_TESTS'] = '1'
	env['INTEG_NAME'] = func.__module__
	env['INTEG_FUNC'] = func.__name__
	with tempfile.NamedTemporaryFile() as tf:
		env['INTEG_OUTPUT'] = tf.name
		tf.write(b'')
		run_sublime(env, *files)
		return tf.read()