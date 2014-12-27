import re

def get_last_part(sig):
	return re.match(r'([A-Z].*?\.)*(.*)$', sig).group(2)

class ExtraGhciCommands(object):
	def __init__(self, commands):
		self._commands = commands

	def on_loaded(self):
		return self._commands.on_loaded()

	def type_or_kind_of(self, sig):
		last_part = get_last_part(sig) 
		return (self
			.type_of(sig)
			.or_else(lambda _: self.kind_of(sig)))

	def is_supertype_of(self, subtype, supertype):
		msg = '((let a = a in a) :: ({})) :: ({})'.format(supertype, subtype)
		return self._commands.type_of(msg).successful()

	def close(self):
		self._commands.close()

	def loaded(self):
		return self._commands.loaded()

	def completions(self, prefix):
		return self._commands.completions(prefix)

	def type_of(self, expr):
		return self._commands.type_of(expr)

	def kind_of(self, expr):
		return self._commands.kind_of(expr)

	def load_haskell_file(self, file_name):
		return self._commands.load_haskell_file(file_name)

	def reload(self):
		return self._commands.reload()

	def run_expr(self, expr):
		return self._commands.run_expr(expr)