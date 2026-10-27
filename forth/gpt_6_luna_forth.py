"""Evaluator for a small, integer-only subset of Forth."""
import re

_NUMBER = re.compile(r"^-?\d+$")
def _is_number(token):
    return bool(_NUMBER.match(token))
class StackUnderflowError(Exception):
    """Raised when a Forth word needs more values than the stack contains."""


def evaluate(input_data):
    """Evaluate a whitespace-separated Forth program and return its stack."""
    stack = []
    dictionary = {}

    def underflow(word, size):
        if len(stack) < size:
            raise StackUnderflowError(
                f"Insufficient number of items in stack"
            )

    def primitive(name):
        def run():
            if name in ("+", "-", "*", "/"):
                underflow(name, 2)
                right = stack.pop()
                left = stack.pop()
                if name == "+":
                    stack.append(left + right)
                elif name == "-":
                    stack.append(left - right)
                elif name == "*":
                    stack.append(left * right)
                else:
                    if right == 0:
                        raise ZeroDivisionError("divide by zero")
                    quotient = abs(left) // abs(right)
                    stack.append(-quotient if (left < 0) != (right < 0) else quotient)
            elif name == "DUP":
                underflow(name, 1)
                stack.append(stack[-1])
            elif name == "DROP":
                underflow(name, 1)
                stack.pop()
            elif name == "SWAP":
                underflow(name, 2)
                stack[-1], stack[-2] = stack[-2], stack[-1]
            elif name == "OVER":
                underflow(name, 2)
                stack.append(stack[-2])

        return run

    for name in ("+", "-", "*", "/", "DUP", "DROP", "SWAP", "OVER"):
        dictionary[name] = primitive(name)

    def execute(token, words):
        if  _is_number(token):
            stack.append(int(token))
            return
        operation = words.get(token.upper())
        if operation is None:
            raise ValueError(f"undefined operation")
        operation()

    tokens = " ".join(input_data).split() if not isinstance(input_data, str) else input_data.split()
    #tokens = input_data.split()
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token != ":":
            execute(token, dictionary)
            index += 1
            continue

        if index + 1 >= len(tokens):
            raise ValueError("word definition is missing a name")
        name = tokens[index + 1]
        if name == ";" or (name.isascii() and name.isdigit()):
            raise ValueError("illegal operation")

        end = index + 2
        while end < len(tokens) and tokens[end] != ";":
            end += 1
        if end == len(tokens):
            raise ValueError(f"definition for {name} is missing ';'")

        # Capture the dictionary as it exists now, so later redefinitions do
        # not change the meaning of words already used in this definition.
        previous_words = dictionary.copy()
        body = tuple(tokens[index + 2 : end])

        def defined_word(body=body, previous_words=previous_words):
            for body_token in body:
                execute(body_token, previous_words)

        dictionary[name.upper()] = defined_word
        index = end + 1

    return stack
