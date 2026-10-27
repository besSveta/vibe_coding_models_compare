class InputCell:
    def __init__(self, initial_value):
        self._value = initial_value
        self._observers = []

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self._value != new_value:
            self._value = new_value
            self._notify()

    def set_value(self, value):
        self.value = value

    def _notify(self):
        for observer in self._observers:
            observer.update()


class ComputeCell:
    def __init__(self, inputs, compute_function):
        self._inputs = inputs
        self._compute_function = compute_function
        self._callbacks = []
        self._observers = []
        self._value = None
        self._updating = False
        
        # Register as observer of input cells
        for input_cell in inputs:
            input_cell._observers.append(self)
        
        # Compute initial value
        self._recompute()

    @property
    def value(self):
        return self._value

    def _recompute(self):
        new_value = self._compute_function([cell.value for cell in self._inputs])
        if new_value != self._value:
            self._value = new_value
            return True
        return False

    def update(self):
        if self._updating:
            return
        
        self._updating = True
        changed = self._recompute()
        self._updating = False
        
        if changed:
            # Notify observers first (for chained compute cells)
            for observer in self._observers:
                observer.update()
            # Then call callbacks
            for callback in self._callbacks:
                callback(self._value)

    def add_callback(self, callback):
        self._callbacks.append(callback)

    def remove_callback(self, callback):
        if callback in self._callbacks:
            self._callbacks.remove(callback)