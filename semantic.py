symbol_table = {}

def evaluate_expression(expr):
    if isinstance(expr, int):
        return expr

    if isinstance(expr, tuple):

        # Variable
        if expr[0] == 'var':
            var = expr[1]
            if var not in symbol_table:
                raise Exception(f"Semantic Error: Variable '{var}' not declared")
            return symbol_table[var]

        # Operations
        left = evaluate_expression(expr[1])
        right = evaluate_expression(expr[2])

        if expr[0] == '+':
            return left + right
        elif expr[0] == '-':
            return left - right
        elif expr[0] == '*':
            return left * right
        elif expr[0] == '/':
            if right == 0:
                raise Exception("Semantic Error: Division by zero")
            return left // right

    return expr


def semantic_analysis(ast):
    symbol_table.clear()

    for node in ast:
        if node[0] == 'declare':
            var = node[1]
            value = evaluate_expression(node[2])
            symbol_table[var] = value

        elif node[0] == 'print':
            value = evaluate_expression(node[1])
            print(f"Output: {value}")