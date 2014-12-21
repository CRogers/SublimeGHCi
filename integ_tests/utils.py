import os, os.path, subprocess

path = '/Applications/Sublime Text.app/Contents/MacOS/Sublime Text'

def wait_until_sublime_closes(popen):
	while not popen.poll():
		try:
			popen.wait(0.1)
			break
		except subprocess.TimeoutExpired:
			pass

def run_sublime(env, path_to_open):
	p = subprocess.Popen([path, path_to_open], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	wait_until_sublime_closes(p)

def run_integ_test(func):
	env = os.environ.copy()
	env['INTEG_TESTS'] = '1'
	env['INTEG_NAME'] = func.__module__
	env['INTEG_FUNC'] = func.__name__
	env['INTEG_OUTPUT'] = os.path.abspath('integ_results')
	with open('integ_results', 'w+') as f:
		f.write('')
	run_sublime(env, 'integ_tests/Completions/Completions1.hs')
	with open('integ_results', 'r') as f:
		return f.read()