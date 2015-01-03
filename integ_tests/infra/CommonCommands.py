class AddResult(object):
    name = 'add_result'

    def perform(self, context):
        context.results().add_last_result()

    def undo(self, context):
        pass