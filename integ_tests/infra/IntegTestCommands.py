from SublimeGHCi.integ_tests.infra.ViewIntegTest import ViewContext, ViewIntegTest

class AddFolder():
    name = 'add_folder'

    def __init__(self, folder_path):
        self._folder_path = folder_path

    def perform(self, context):
        project_data = context.window().project_data()
        project_data['folders'].append({'path': self._folder_path})
        context.window().set_project_data(project_data)

class WithFile():
    name = 'with_file'

    def __init__(self, file_name, with_view_test):
        self._file_name = file_name
        self._view_test = with_view_test(ViewIntegTest())

    def perform(self, context):
        view = context.window().open_file()
        view_context = ViewContext(context, view)
        self._view_test.run(view_context)