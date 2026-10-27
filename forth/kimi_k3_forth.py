class StackUnderflowError(Exception):
    """Exception raised when the stack does not contain enough items."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message


def evaluate(input_data):
    stack = []
    definitions = {}

    def is_number(token):
        return token.isdigit() or (token.startswith('-') and token[1:].isdigit())

    def binary_op(operation):
        if len(stack) < 2:
            raise StackUnderflowError("Insufficient number of items in stack")
        b = stack.pop()
        a = stack.pop()
        stack.append(operation(a, b))

    def divide(a, b):
        if b == 0:
            raise ZeroDivisionError("divide by zero")
        return int(a / b)

    builtins = {
        '+': lambda: binary_op(lambda a, b: a + b),
        '-': lambda: binary_op(lambda a, b: a - b),
        '*': lambda: binary_op(lambda a, b: a * b),
        '/': lambda: binary_op(divide),
        'dup': lambda: stack.append(stack[-1]) if stack else (_ for _ in ()).throw(StackUnderflowError("Insufficient number of items in stack")),
        'drop': lambda: stack.pop() if stack else (_ for _ in ()).throw(StackUnderflowError("Insufficient number of items in stack")),
        'swap': lambda: (stack.append(stack.pop(-2))) if len(stack) >= 2 else (_ for _ in ()).throw(StackUnderflowError("Insufficient number of items in stack")),
        'over': lambda: (stack.append(stack[-2])) if len(stack) >= 2 else (_ for _ in ()).throw(StackUnderflowError("Insufficient number of items in stack")),
    }

    def process_tokens(tokens):
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == ':':
                if i + 2 >= len(tokens):
                    raise ValueError("invalid definition")
                name = tokens[i + 1]
                if is_number(name):
                    raise ValueError("illegal operation")
                end = tokens.index(';', i + 2)
                definitions[name] = tokens[i + 2:end]
                i = end + 1
            elif is_number(token):
                stack.append(int(token))
                i += 1
            elif token in definitions:
                process_tokens(definitions[token])
                i += 1
            elif token in builtins:
                builtins[token]()
                i += 1
            else:
                raise ValueError("undefined operation")

    for line in input_data:
        tokens = line.lower().split()
        process_tokens(tokens)

    return stack