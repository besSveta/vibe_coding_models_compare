class InputCell:
    def __init__(self, initial_value):
        self._value = initial_value
        self.observers = []

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value != self._value:
            self._value = new_value
            for observer in self.observers:
                observer.notify()


class ComputeCell:
    def __init__(self, inputs, compute_function):
        self.inputs = list(inputs)
        self.compute_function = compute_function
        self.callbacks = []
        self.observers = []
        self.value = self.compute_function([i.value for i in self.inputs])
        for cell in self.inputs:
            cell.observers.append(self)
        self._stable_value = self.value

    def notify(self):
        old = self.value
        self.value = self.compute_function([i.value for i in self.inputs])
        if self.value != old:
            for cb in self.callbacks:
                cb(self.value)

    def add_callback(self, callback):
        self.callbacks.append(callback)

    def remove_callback(self, callback):
        if callback in self.callbacks:
            self.callbacks.remove(callback)