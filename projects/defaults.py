import sublime

from SublimeGHCi.projects.ProjectManager import *
from SublimeGHCi.projects.WindowInfo import *
from SublimeGHCi.projects.ProjectFileDetector import *

def default_project_manager():
	return ProjectManager(WindowInfo(sublime), ProjectFileDetector())