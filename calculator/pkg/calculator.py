# calculator/pkg/calculator.py


class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
            "!": lambda a: self._factorial(a),  # Factorial operator
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "!": 3,  # Highest precedence for factorial
        }

    def _factorial(self, n):
        if not isinstance(n, (int, float)) or n < 0 or n != int(n):
            raise ValueError("Factorial is only defined for non-negative integers")
        n = int(n)
        if n == 0:
            return 1
        res = 1
        for i in range(1, n + 1):
            res *= i
        return res

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = self._tokenize(expression)  # Use a tokenizer to handle '!' next to numbers
        return self._evaluate_infix(tokens)

    def _tokenize(self, expression):
        # This tokenizer will handle numbers and operators, including '!'
        # It assumes that '!' will immediately follow a number or closing parenthesis.
        tokens = []
        i = 0
        while i < len(expression):
            if expression[i].isspace():
                i += 1
                continue
            if expression[i].isdigit():
                j = i
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                tokens.append(expression[i:j])
                i = j
                continue
            if expression[i] in self.operators:
                tokens.append(expression[i])
                i += 1
                continue
            if expression[i] == '(' or expression[i] == ')': # Added parenthesis support for future extensibility, though not strictly needed for factorial
                tokens.append(expression[i])
                i += 1
                continue
            raise ValueError(f"Invalid character: {expression[i]}")
        return tokens

    def _evaluate_infix(self, tokens):
        values = []
        operators = []

        for token in tokens:
            if token in self.operators:
                if token == '!': # Handle factorial immediately as a unary operator
                    if not values:
                        raise ValueError("Factorial operator requires an operand")
                    operand = values.pop()
                    values.append(self.operators[token](operand))
                else: # Binary operators
                    while (
                        operators
                        and operators[-1] in self.precedence
                        and self.precedence[operators[-1]] >= self.precedence[token]
                    ):
                        self._apply_operator(operators, values)
                    operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    self._apply_operator(operators, values)
                if not operators or operators[-1] != '(':
                    raise ValueError("Mismatched parentheses")
                operators.pop() # Pop '('
            else:
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"invalid token: {token}")

        while operators:
            if operators[-1] == '(':
                raise ValueError("Mismatched parentheses")
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("invalid expression")

        return values[0]

    def _apply_operator(self, operators, values):
        if not operators:
            return

        operator = operators.pop()
        if operator == '!': # This should ideally be handled immediately in the loop, but as a safeguard.
            if len(values) < 1:
                raise ValueError(f"not enough operands for operator {operator}")
            operand = values.pop()
            values.append(self.operators[operator](operand))
        else: # Binary operators
            if len(values) < 2:
                raise ValueError(f"not enough operands for operator {operator}")
            b = values.pop()
            a = values.pop()
            values.append(self.operators[operator](a, b))
