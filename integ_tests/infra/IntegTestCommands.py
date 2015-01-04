import os.path

from SublimeGHCi.integ_tests.infra.ViewIntegTestCommands import Wait
from SublimeGHCi.integ_tests.infra.ViewIntegTest import ViewContext, ViewIntegTest

empty_project_data = {'folders': []}

def absolute_path(path):
    return os.path.abspath(os.path.join('SublimeGHCi/integ_tests/', path))

class AddFolder():
    name = 'add_folder'

    def __init__(self, folder_path):
        self._folder_path = absolute_path(folder_path)

    def perform(self, context):
        project_data = context.window().project_data()
        if project_data == None:
            project_data = empty_project_data
        project_data['folders'].append({'path': self._folder_path})
        context.window().set_project_data(project_data)

class WithFile():
    name = 'with_file'

    def __init__(self, file_name, with_view_test):
        self._file_name = absolute_path(file_name)
        self._view_test = with_view_test(ViewIntegTest())

    def _open_file(self, context):
        view = context.window().open_file(self._file_name)
        view_context = ViewContext(context, view)
        Wait().perform(view_context)
        return view_context

    def perform(self, context):
        view_context = self._open_file(context)
        self._view_test.perform(view_context)