class StackUnderflowError(Exception):
    """Exception raised when the stack does not contain enough items for an operation."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

def evaluate(input_data):
    stack = []
    definitions = {}

    def is_number(tok):
        return tok.isdigit()

    tokens = input_data.split()

    i = 0
    n = len(tokens)

    def run_tokens(token_list):
        for tok in token_list:
            if is_number(tok):
                stack.append(int(tok))
                continue
            word = tok.lower()
            if word in definitions:
                # Expand definition (recursively execute its tokens)
                run_tokens(definitions[word])
                continue
            # Stack manipulation
            if word == 'dup':
                if len(stack) < 1:
                    raise StackUnderflowError("Insufficient number of items in stack")
                stack.append(stack[-1])
                continue
            if word == 'drop':
                if len(stack) < 1:
                    raise StackUnderflowError("Insufficient number of items in stack")
                stack.pop()
                continue
            if word == 'swap':
                if len(stack) < 2:
                    raise StackUnderflowError("Insufficient number of items in stack")
                stack[-1], stack[-2] = stack[-2], stack[-1]
                continue
            if word == 'over':
                if len(stack) < 2:
                    raise StackUnderflowError("Insufficient number of items in stack")
                stack.append(stack[-2])
                continue
            # Arithmetic
            if word in ('+', '-', '*', '/'):
                if len(stack) < 2:
                    raise StackUnderflowError("Insufficient number of items in stack")
                b = stack.pop()
                a = stack.pop()
                if word == '+':
                    stack.append(a + b)
                elif word == '-':
                    stack.append(a - b)
                elif word == '*':
                    stack.append(a * b)
                else:  # '/'
                    if b == 0:
                        raise ZeroDivisionError("divide by zero")
                    # integer division truncated toward zero
                    stack.append(int(a / b))
                continue
            # Unknown word
            raise ValueError("undefined operation")

    while i < n:
        tok = tokens[i]
        if tok == '':
            i += 1
            continue
        if tok == ':':
            # start definition
            i += 1
            if i >= n:
                raise ValueError("invalid definition")
            name = tokens[i].lower()
            if is_number(name):
                raise ValueError("invalid word")
            i += 1
            body = []
            # collect until ';'
            while i < n and tokens[i] != ';':
                body.append(tokens[i])
                i += 1
            if i >= n or tokens[i] != ';':
                raise ValueError("invalid definition")
            # store definition with tokens as they appeared (case-insensitive handling in run)
            # convert body tokens to lower-case for words to ensure case-insensitivity
            definitions[name] = [t if is_number(t) else t.lower() for t in body]
            i += 1
        else:
            # normal token: execute it
            run_tokens([tok])
            i += 1

    return stack