class ProjectFileDetector(object):
	def __init__(self, glob):
		self._glob = glob.glob

	def _has_file(self, path, file):
		matches = self._glob('{}/{}'.format(path, file))
		return len(matches) != 0

	def has_cabal_file(self, path):
		return self._has_file(path, '*.cabal')

	def has_default_nix_file(self, path):
		return self._has_file(path, 'default.nix')