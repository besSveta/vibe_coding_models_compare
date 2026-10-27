
class InputCell:
    def __init__(self, initial_value):
        self._value = initial_value
        self._dependents = set()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value == self._value:
            return
        self._value = new_value
        _propagate(self)


class ComputeCell:
    def __init__(self, inputs, compute_function):
        self.inputs = list(inputs)
        self.compute_function = compute_function
        self._dependents = set()
        self._callbacks = []

        for cell in self.inputs:
            cell._dependents.add(self)

        self._value = self._compute()

    @property
    def value(self):
        return self._value

    #def _compute(self):
        #return self.compute_function(*(cell.value for cell in self.inputs))

    def _compute(self):
        return self.compute_function([cell.value for cell in self.inputs])

    def add_callback(self, callback):
        self._callbacks.append(callback)

    def remove_callback(self, callback):
        try:
            self._callbacks.remove(callback)
        except ValueError:
            pass


def _propagate(changed_cell):
    affected = set()
    stack = [changed_cell]

    while stack:
        cell = stack.pop()
        for dependent in cell._dependents:
            if dependent not in affected:
                affected.add(dependent)
                stack.append(dependent)

    if not affected:
        return

    order = []
    visited = set()

    def visit(cell):
        if cell in visited:
            return
        visited.add(cell)

        for input_cell in cell.inputs:
            if isinstance(input_cell, ComputeCell) and input_cell in affected:
                visit(input_cell)

        order.append(cell)

    for cell in affected:
        visit(cell)

    old_values = {}
    new_values = {}

    for cell in order:
        old_values[cell] = cell._value
        cell._value = cell._compute()
        new_values[cell] = cell._value

    for cell in order:
        if old_values[cell] != new_values[cell]:
            for callback in list(cell._callbacks):
                callback(new_values[cell])