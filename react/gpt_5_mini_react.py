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
        self._propagate()

    def _propagate(self):
        queue = list(self._dependents)
        visited = set()
        changed = []

        while queue:
            cell = queue.pop(0)
            if id(cell) in visited:
                continue
            visited.add(id(cell))

            new_val = cell._compute_value()
            if new_val != cell._value:
                cell._value = new_val
                changed.append(cell)
                queue.extend(cell._dependents)

        for cell in changed:
            for cb in list(cell._callbacks):
                try:
                    cb(cell._value)
                except Exception:
                    pass


class ComputeCell:
    def __init__(self, inputs, compute_function):
        self._inputs = list(inputs)
        self._compute = compute_function
        self._dependents = []
        self._callbacks = []
        # register as dependent on inputs
        for inp in self._inputs:
            if not hasattr(inp, "_dependents"):
                inp._dependents = []
            inp._dependents.append(self)
        # initial value
        self._value = self._compute_value()

    @property
    def value(self):
        return self._value

    def _compute_value(self):
        vals = [inp.value for inp in self._inputs]
        try:
            return self._compute(*vals)
        except TypeError:
            return self._compute(vals)

    def add_callback(self, callback):
        if callback not in self._callbacks:
            self._callbacks.append(callback)

    def remove_callback(self, callback):
        if callback in self._callbacks:
            self._callbacks.remove(callback)