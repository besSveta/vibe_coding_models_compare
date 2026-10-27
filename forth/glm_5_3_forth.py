class StackUnderflowError(Exception):
    """Exception raised when the stack has insufficient items."""
    def __init__(self, message="Insufficient number of items in stack"):
        self.message = message
        super().__init__(self.message)


def evaluate(input_data):
    if isinstance(input_data, str):
        input_data = [input_data]

    definitions = {}
    stack = []

    def resolve_word(word):
        seen = set()
        while word in definitions and word not in seen:
            seen.add(word)
            word = definitions[word]
        if word in seen:
            raise ValueError("undefined operation")
        return word

    def parse_number(token):
        if token.isdigit():
            return int(token)
        return None

    def apply_token(token):
        token = token.upper()
        num = parse_number(token)
        if num is not None:
            stack.append(num)
            return
        word = resolve_word(token)
        if word.isdigit():
            stack.append(int(word))
            return
        if word == "+":
            if len(stack) < 2:
                raise StackUnderflowError("Insufficient number of items in stack")
            b, a = stack.pop(), stack.pop()
            stack.append(a + b)
        elif word == "-":
            if len(stack) < 2:
                raise StackUnderflowError("Insufficient number of items in stack")
            b, a = stack.pop(), stack.pop()
            stack.append(a - b)
        elif word == "*":
            if len(stack) < 2:
                raise StackUnderflowError("Insufficient number of items in stack")
            b, a = stack.pop(), stack.pop()
            stack.append(a * b)
        elif word == "/":
            if len(stack) < 2:
                raise StackUnderflowError("Insufficient number of items in stack")
            b, a = stack.pop(), stack.pop()
            if b == 0:
                raise ZeroDivisionError("divide by zero")
            stack.append(int(a / b))
        elif word == "DUP":
            if not stack:
                raise StackUnderflowError("Insufficient number of items in stack")
            stack.append(stack[-1])
        elif word == "DROP":
            if not stack:
                raise StackUnderflowError("Insufficient number of items in stack")
            stack.pop()
        elif word == "SWAP":
            if len(stack) < 2:
                raise StackUnderflowError("Insufficient number of items in stack")
            stack[-1], stack[-2] = stack[-2], stack[-1]
        elif word == "OVER":
            if len(stack) < 2:
                raise StackUnderflowError("Insufficient number of items in stack")
            stack.append(stack[-2])
        else:
            raise ValueError("undefined operation")

    for line in input_data:
        tokens = line.split()
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == ":":
                if i + 2 >= len(tokens) or tokens[i + 2] != ";":
                    # allow multi-token definitions
                    name = tokens[i + 1]
                    end = tokens.index(";", i + 2)
                    body = tokens[i + 2:end]
                    definitions[name.upper()] = body
                    i = end + 1
                    continue
                name = tokens[i + 1]
                definitions[name.upper()] = tokens[i + 2]
                i += 4
                continue
            apply_token(token)
            i += 1

    return stack

# class StackUnderflowError(Exception):
#     """Exception raised when the stack has insufficient items."""
#     def __init__(self, message="Insufficient number of items in stack"):
#         self.message = message
#         super().__init__(self.message)
#
#
# def evaluate(input_data):
#     if isinstance(input_data, str):
#         input_data = [input_data]
#
#     definitions = {}
#     stack = []
#
#     def apply_token(token):
#         token = token.upper()
#         if token.isdigit():
#             stack.append(int(token))
#             return
#         if token in definitions:
#             for t in definitions[token]:
#                 apply_token(t)
#             return
#         if token == "+":
#             if len(stack) < 2:
#                 raise StackUnderflowError("Insufficient number of items in stack")
#             b, a = stack.pop(), stack.pop()
#             stack.append(a + b)
#         elif token == "-":
#             if len(stack) < 2:
#                 raise StackUnderflowError("Insufficient number of items in stack")
#             b, a = stack.pop(), stack.pop()
#             stack.append(a - b)
#         elif token == "*":
#             if len(stack) < 2:
#                 raise StackUnderflowError("Insufficient number of items in stack")
#             b, a = stack.pop(), stack.pop()
#             stack.append(a * b)
#         elif token == "/":
#             if len(stack) < 2:
#                 raise StackUnderflowError("Insufficient number of items in stack")
#             b, a = stack.pop(), stack.pop()
#             if b == 0:
#                 raise ZeroDivisionError("divide by zero")
#             stack.append(int(a / b))
#         elif token == "DUP":
#             if not stack:
#                 raise StackUnderflowError("Insufficient number of items in stack")
#             stack.append(stack[-1])
#         elif token == "DROP":
#             if not stack:
#                 raise StackUnderflowError("Insufficient number of items in stack")
#             stack.pop()
#         elif token == "SWAP":
#             if len(stack) < 2:
#                 raise StackUnderflowError("Insufficient number of items in stack")
#             stack[-1], stack[-2] = stack[-2], stack[-1]
#         elif token == "OVER":
#             if len(stack) < 2:
#                 raise StackUnderflowError("Insufficient number of items in stack")
#             stack.append(stack[-2])
#         else:
#             raise ValueError("undefined operation")
#
#     for line in input_data:
#         tokens = line.split()
#         i = 0
#         while i < len(tokens):
#             token = tokens[i]
#             if token == ":":
#                 name = tokens[i + 1].upper()
#                 if name.isdigit():
#                     raise ValueError("cannot redefine a number")
#                 end = tokens.index(";", i + 2)
#                 body = tokens[i + 2:end]
#                 definitions[name] = [t.upper() for t in body]
#                 i = end + 1
#                 continue
#             apply_token(token)
#             i += 1
#
#     return stack