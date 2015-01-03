class Results():
    def __init__(self):
        self._last_result = None
        self._results = []

    def set_last_result(self, result):
        self._last_result = result

    def add_last_result(self):
        self._results.append(self._last_result)

    def all_results(self):
        return self._results