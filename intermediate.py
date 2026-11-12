temp_count = 0

def new_temp():
    global temp_count
    temp_count += 1
    return f"t{temp_count}"


def generate_tac_expr(expr, code):
    if isinstance(expr, int):
        return str(expr)

    if isinstance(expr, tuple):

        if expr[0] == 'var':
            return expr[1]

        left = generate_tac_expr(expr[1], code)
        right = generate_tac_expr(expr[2], code)

        temp = new_temp()
        code.append(f"{temp} = {left} {expr[0]} {right}")
        return temp

    return str(expr)


def generate_tac(ast):
    global temp_count
    temp_count = 0

    code = []

    for node in ast:

        if node[0] == 'declare':
            var = node[1]
            result = generate_tac_expr(node[2], code)
            code.append(f"{var} = {result}")

        elif node[0] == 'print':
            result = generate_tac_expr(node[1], code)
            code.append(f"print {result}")

    return code