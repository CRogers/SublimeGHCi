from glob import glob

class ProjectFileDetector(object):
	def _has_file(self, path, file):
		print('{}/{}'.format(path, file))
		matches = glob('{}/{}'.format(path, file))
		return len(matches) != 0

	def has_cabal_file(self, path):
		return self._has_file(path, '*.cabal')

	def has_default_nix_file(self, path):
		return self._has_file(path, 'default.nix')