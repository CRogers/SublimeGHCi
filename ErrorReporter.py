from SublimeGHCi.OutputPanel import OutputPanel

class ErrorReporter(object):
	def __init__(self):
		self.__output_panel = OutputPanel('sublime_ghci')

	def report_errors(self, error_message):
		self.__output_panel.display_text(error_message)
		pass

	def clear_errors(self):
		self.__output_panel.hide()
		pass