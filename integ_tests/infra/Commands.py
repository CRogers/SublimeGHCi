from SublimeGHCi.integ_tests.infra.ViewIntegTest import *

class AddFolder(object):
    name = 'add_folder'

    def __init__(self, folder_path):
        self._folder_path = folder_path

    def perform(self, context):
        window = context.window()
        project_data = window.project_data()
        project_data['folders'].append({'path': self._folder_path})
        window.set_project_data(project_data)

    def undo(self, context):
        pass

class OpenFile(object):
    name = 'open_file'

    def __init__(self, file_name):
        self._file_name = file_name
        self._view_integ_test = None

    def next(self, integ_test):
        self._view_integ_test = ViewIntegTest(integ_test)
        return self._view_integ_test

    def _open_file(self, context):
        view = context.window().open_file(self._file_name)
        return ViewContext(context, view)

    def perform(self, context):
        view_context = self._open_file(context)
        self._view_integ_test.perform(view_context)

    def undo(self, context):
        view_context = self._open_file(context)
        self._view_integ_test.undo(view_context)
        context.window().run_command('close')