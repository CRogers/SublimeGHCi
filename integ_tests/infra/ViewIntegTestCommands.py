import time

class AddResult(object):
    name = 'add_result'

    def perform(self, context):
        context.results().add_last_result()

class Sleep(object):
    name = 'sleep'

    def __init__(self, seconds):
        self._seconds = seconds

    def perform(self, context):
        time.sleep(self._seconds)

class IsVisible():
    name = 'is_visible'

    def perform(self, context):
        output_panel = context.top().output_panel_factory.output_panel_for_window(context.window())
        return output_panel._testing_is_shown()

class Text():
    name = 'text'

    def perform(self, context):
        end = context.view().size()
        region = context.sublime().Region(0, end)
        return context.view().substr(region)

class AppendText(object):
    name = 'append_text'

    def __init__(self, string):
        self._string = string

    def perform(self, context):
        end = context.view().size()
        context.view().run_command('insert_text', {'point': end, 'string': self._string})

class DeleteRange():
    name = 'delete_range'

    def __init__(self, start, length):
        self._start = start
        self._length = length

    def perform(self, context):
        print('delete_range')
        context.view().run_command('sublime_ghci_erase_text', {'start': self._start, 'length': self._length})

class DeleteLeftFromEnd():
    name = 'delete_left_from_end'

    def __init__(self, times = 0):
        self._times = times

    def perform(self, context):
        end = context.view().size()
        DeleteRange(end - self._times, self._times).perform(context)

class MessageDialog():
    name = 'message_dialog'

    def __init__(self, message):
        self._message = message

    def perform(self, context):
        context.sublime().message_dialog(self._message)

class Save(object):
    name = 'save'

    def perform(self, context):
        context.view().run_command('save')

class Wait(object):
    name = 'wait'

    def perform(self, context):
        while context.view().is_loading() or not context.top().manager.loaded(context.view()):
            time.sleep(0.1)

class Complete(object):
    name = 'complete'

    def __init__(self, string):
        self._string = string

    def _complete(self, context):
        end = context.view().size()
        return context.top().manager.complete(context.view(), self._string, end)

    def perform(self, context):
        AppendText(self._string).perform(context)
        self._complete(context)
        Wait().perform(context)
        return self._complete(context)