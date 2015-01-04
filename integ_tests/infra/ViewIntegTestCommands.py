import time

class AddResult(object):
	name = 'add_result'

	def perform(self, context):
		context.results().add_last_result()

	def undo(self, context):
		pass

class AppendText(object):
	name = 'append_text'

	def __init__(self, string):
		self._string = string

	def perform(self, context):
		end = context.view().size()
		context.view().run_command('insert_text', {'point': end, 'string': self._string})

	def undo(self, context):
		context.view().run_command('undo')

class DeleteRange():
	name = 'delete_range'

	def __init__(self, start, length):
		self._start = start
		self._length = length
		self._deleted = None

	def perform(self, context):
		context.view().substr(context.sublime().Range(self._start, self._length))

	def undo(self, context):
		pass

class Save(object):
	name = 'save'

	def perform(self, context):
		context.view().run_command('save')

	def undo(self, context):
		pass

class Wait(object):
	name = 'wait'

	def perform(self, context):
		while not context.manager().loaded(context.view()):
			time.sleep(0.1)

	def undo(self, context):
		pass

class Complete(object):
	name = 'complete'

	def __init__(self, string):
		self._string = string
		self._append = AppendText(self._string)

	def _complete(self, context):
		end = context.view().size()
		return context.manager().complete(context.view(), self._string, end)

	def perform(self, context):
		self._append.perform(context)
		self._complete(context)
		Wait().perform(context)
		return self._complete(context)

	def undo(self, context):
		self._append.undo(context)