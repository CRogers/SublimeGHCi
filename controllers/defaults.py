from SublimeGHCi.controllers.ControllerFactory import *
from SublimeGHCi.controllers.CachingControllerFactory import *

def default_controller_factory(project_manager, ghci_factory, completor_factory, error_reporter):
	return CachingControllerFactory(ControllerFactory(project_manager, ghci_factory, completor_factory, error_reporter))