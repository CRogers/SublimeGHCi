import re

def get_last_part(sig):
	return re.match(r'([A-Z].*?\.)*(.*)$', sig).group(2)

class ExtraGhciCommands(object):
	def __init__(self, commands):
		self._commands = commands

	def type_or_kind_of(self, sig):
		last_part = get_last_part(sig) 
		return (self._commands
			.type_of(sig)
			.or_else(lambda _: self.commands.kind_of(sig)))