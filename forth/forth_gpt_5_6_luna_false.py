"""A small evaluator for the Forth exercise."""


class StackUnderflowError(Exception):
    """Raised when an operation needs more values than the stack contains."""


_UNDERFLOW = "Insufficient number of items in stack"


def _is_number(token):
    """Return whether *token* is a signed decimal integer."""
    if not token:
        return False
    digits = token[1:] if token[0] == "-" else token
    return bool(digits) and digits.isascii() and digits.isdigit()


def evaluate(input_data):
    """Evaluate Forth source supplied as a list of input lines."""
    tokens = " ".join(input_data).split() if not isinstance(input_data, str) else input_data.split()
    definitions = {}
    stack = []

    def require(count):
        if len(stack) < count:
            raise StackUnderflowError(_UNDERFLOW)

    def execute(words):
        for token in words:
            if _is_number(token):
                stack.append(int(token))
                continue

            word = token.lower()
            if word in definitions:
                execute(definitions[word])
            elif word == "+":
                require(2)
                right = stack.pop()
                stack.append(stack.pop() + right)
            elif word == "-":
                require(2)
                right = stack.pop()
                stack.append(stack.pop() - right)
            elif word == "*":
                require(2)
                right = stack.pop()
                stack.append(stack.pop() * right)
            elif word == "/":
                require(2)
                right = stack.pop()
                left = stack.pop()
                if right == 0:
                    raise ZeroDivisionError("divide by zero")
                quotient = abs(left) // abs(right)
                stack.append(-quotient if (left < 0) != (right < 0) else quotient)
            elif word == "dup":
                require(1)
                stack.append(stack[-1])
            elif word == "drop":
                require(1)
                stack.pop()
            elif word == "swap":
                require(2)
                stack[-1], stack[-2] = stack[-2], stack[-1]
            elif word == "over":
                require(2)
                stack.append(stack[-2])
            else:
                raise ValueError("undefined operation")

    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token != ":":
            execute([token])
            index += 1
            continue

        index += 1
        if index >= len(tokens):
            raise ValueError("invalid definition")
        name = tokens[index]
        if _is_number(name):
            raise ValueError("illegal operation")
        name = name.lower()
        index += 1

        body = []
        while index < len(tokens) and tokens[index] != ";":
            body.append(tokens[index])
            index += 1
        if index == len(tokens):
            raise ValueError("invalid definition")

        # Compile references to already-defined words now.  This makes a
        # redefinition able to use the previous meaning of its own name and
        # keeps earlier definitions independent of later redefinitions.
        expanded = []
        for word in body:
            previous = definitions.get(word.lower())
            if previous is None:
                expanded.append(word)
            else:
                expanded.extend(previous)
        definitions[name] = expanded
        index += 1

    return stack
