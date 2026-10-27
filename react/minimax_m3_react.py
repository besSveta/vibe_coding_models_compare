class InputCell:
    def __init__(self, initial_value):
        self._value = initial_value
        self._dependents = []

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value == self._value:
            return

        self._value = new_value
        self._notify_dependents()

    def _add_dependent(self, cell):
        if cell not in self._dependents:
            self._dependents.append(cell)

    def _remove_dependent(self, cell):
        if cell in self._dependents:
            self._dependents.remove(cell)

    def _notify_dependents(self):
        for cell in list(self._dependents):
            cell._recalculate()


class ComputeCell:
    def __init__(self, inputs, compute_function):
        self._inputs = list(inputs)
        self._compute_function = compute_function
        self._callbacks = []
        self._value = self._compute()

        for input_cell in self._inputs:
            input_cell._add_dependent(self)

    @property
    def value(self):
        return self._value

    def add_callback(self, callback):
        if callback not in self._callbacks:
            self._callbacks.append(callback)

    def remove_callback(self, callback):
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def _recalculate(self):
        new_value = self._compute()
        if new_value == self._value:
            return

        self._value = new_value
        for callback in list(self._callbacks):
            callback(self._value)

    def _compute(self):
        return self._compute_function(*(input_cell.value for input_cell in self._inputs))