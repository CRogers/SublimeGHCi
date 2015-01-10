from SublimeGHCi.error_reporters.ErrorReporter import *

class ErrorReporterFactory(object):
    def __init__(self, project_manager, output_panel_factory):
        self._project_manager = project_manager
        self._output_panel_factory = output_panel_factory

    def error_reporter_for_view(self, view):
        project = self._project_manager.project_for_view(view)
        output_panel = self._output_panel_factory.output_panel_for_window(view.window())
        return ErrorReporter(output_panel, project)