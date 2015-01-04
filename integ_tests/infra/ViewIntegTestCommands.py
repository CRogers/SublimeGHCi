import time

class AddResult(object):
	name = 'add_result'

	def perform(self, context):
		context.results().add_last_result()

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

	def perform(self, context):
		print('delete_range')
		context.view().run_command('sublime_ghci_erase_text', {'start': self._start, 'length': self._length})

	def undo(self, context):
		context.view().run_command('undo')

class DeleteLeft():
	name = 'delete_left'

	def __init__(self, times = 0):
		self._times = times

	def perform(self, context):
		for x in range(0, self._times):
			context.view().run_command('left_delete')

	def undo(self, context):
		context.view().run_command('undo')

class Save(object):
	name = 'save'

	def perform(self, context):
		context.view().run_command('save')

class Wait(object):
	name = 'wait'

	def perform(self, context):
		while context.view().is_loading() or not context.manager().loaded(context.view()):
			time.sleep(0.1)

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