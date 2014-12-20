import os
import signal

def quit_sublime():
	os.kill(os.getppid(), signal.SIGTERM)