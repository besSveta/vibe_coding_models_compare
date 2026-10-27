"""A small reactive cell system."""


class InputCell:
    """A cell whose value can be changed directly."""

    def __init__(self, initial_value):
        self._value = initial_value
        self._dependents = set()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        """Set the cell's value and update all dependent compute cells."""
        if value == self._value:
            return
        self._value = value
        _update_dependents(self)


class ComputeCell:
    """A cell whose value is computed from one or more other cells."""

    def __init__(self, inputs, compute_function):
        self._inputs = tuple(inputs)
        self._compute_function = compute_function
        self._dependents = set()
        self._callbacks = []
        self.value = compute_function([cell.value for cell in self._inputs])
        for cell in self._inputs:
            cell._dependents.add(self)

    def add_callback(self, callback):
        """Register a function to call when this cell's value changes."""
        self._callbacks.append(callback)

    def remove_callback(self, callback):
        """Remove a previously registered callback, if present."""
        try:
            self._callbacks.remove(callback)
        except ValueError:
            pass


def _update_dependents(changed_cell):
    """Recompute descendants in dependency order, then notify callbacks.

    Recalculation happens before notification so a callback only observes the
    final values produced by this input update, including through a diamond
    shaped dependency graph.
    """
    affected = set()
    pending = list(changed_cell._dependents)
    while pending:
        cell = pending.pop()
        if cell in affected:
            continue
        affected.add(cell)
        pending.extend(cell._dependents)

    remaining = set(affected)
    changed = []
    while remaining:
        ready = [
            cell
            for cell in remaining
            if all(not isinstance(source, ComputeCell) or source not in remaining
                   for source in cell._inputs)
        ]
        # An acyclic cell graph always has a ready node. The fallback gives a
        # clear failure if callers have manually introduced a dependency cycle.
        if not ready:
            raise ValueError("cyclic compute cell dependencies")

        for cell in ready:
            old_value = cell.value
            new_value = cell._compute_function(
                [source.value for source in cell._inputs]
            )
            cell.value = new_value
            if new_value != old_value:
                changed.append(cell)
        remaining.difference_update(ready)

    for cell in changed:
        for callback in tuple(cell._callbacks):
            callback(cell.value)
