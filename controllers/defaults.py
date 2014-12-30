from SublimeGHCi.controllers.ControllerFactory import *
from SublimeGHCi.controllers.CachingControllerFactory import *

def default_controller_factory(ghci_factory, completor_factory):
	return CachingControllerFactory(ControllerFactory(ghci_factory, completor_factory))