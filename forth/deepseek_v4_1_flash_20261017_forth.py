import re


class StackUnderflowError(Exception):
    """Exception raised when the stack is not full."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


_NUMBER = re.compile(r"^-?\d+$")


def _is_number(token):
    return bool(_NUMBER.match(token))


def evaluate(input_data):
    if isinstance(input_data, str):
        input_data = [input_data]

    tokens = []
    for line in input_data:
        tokens.extend(line.split())

    stack = []
    user_definitions = {}

    def require(count):
        if len(stack) < count:
            raise StackUnderflowError("Insufficient number of items in stack")

    def execute(token):
        if _is_number(token):
            stack.append(int(token))
            return

        name = token.lower()

        if name in user_definitions:
            for definition_token in user_definitions[name]:
                execute(definition_token)
            return

        if name == "+":
            require(2)
            b = stack.pop()
            a = stack.pop()
            stack.append(a + b)

        elif name == "-":
            require(2)
            b = stack.pop()
            a = stack.pop()
            stack.append(a - b)

        elif name == "*":
            require(2)
            b = stack.pop()
            a = stack.pop()
            stack.append(a * b)

        elif name == "/":
            require(2)
            b = stack.pop()
            a = stack.pop()
            if b == 0:
                raise ZeroDivisionError("divide by zero")
            stack.append(a // b)

        elif name == "dup":
            require(1)
            stack.append(stack[-1])

        elif name == "drop":
            require(1)
            stack.pop()

        elif name == "swap":
            require(2)
            stack[-1], stack[-2] = stack[-2], stack[-1]

        elif name == "over":
            require(2)
            stack.append(stack[-2])

        else:
            raise ValueError("undefined operation")

    index = 0
    while index < len(tokens):
        token = tokens[index]

        if token == ":":
            index += 1
            if index >= len(tokens):
                raise ValueError("illegal operation")

            word_name = tokens[index]
            if _is_number(word_name):
                raise ValueError("illegal operation")

            index += 1
            definition = []

            while index < len(tokens) and tokens[index] != ";":
                definition.append(tokens[index])
                index += 1

            if index >= len(tokens):
                raise ValueError("illegal operation")

            expanded_definition = []

            for definition_token in definition:
                name = definition_token.lower()

                if name in user_definitions:
                    expanded_definition.extend(user_definitions[name])
                else:
                    expanded_definition.append(definition_token)

            user_definitions[word_name.lower()] = expanded_definition
            index += 1

        elif token == ";":
            raise ValueError("illegal operation")

        else:
            execute(token)
            index += 1

    return stack