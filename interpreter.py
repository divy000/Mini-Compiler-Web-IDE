def execute_tac(tac_code):
    memory = {}

    for line in tac_code:
        parts = line.split()

        # ---------------- ASSIGNMENT ----------------
        if '=' in parts:
            var = parts[0]

            # Case: x = value
            if len(parts) == 3:
                value = parts[2]

                if value.isdigit():
                    memory[var] = int(value)
                else:
                    if value not in memory:
                        raise Exception(f"Runtime Error: Variable '{value}' not declared")
                    memory[var] = memory[value]

            # Case: x = y + z
            elif len(parts) == 5:
                left = parts[2]
                op = parts[3]
                right = parts[4]

                # Resolve left operand
                if left.isdigit():
                    left_val = int(left)
                else:
                    if left not in memory:
                        raise Exception(f"Runtime Error: Variable '{left}' not declared")
                    left_val = memory[left]

                # Resolve right operand
                if right.isdigit():
                    right_val = int(right)
                else:
                    if right not in memory:
                        raise Exception(f"Runtime Error: Variable '{right}' not declared")
                    right_val = memory[right]

                # Perform operation
                if op == '+':
                    memory[var] = left_val + right_val
                elif op == '-':
                    memory[var] = left_val - right_val
                elif op == '*':
                    memory[var] = left_val * right_val
                elif op == '/':
                    if right_val == 0:
                        raise Exception("Runtime Error: Division by zero")
                    memory[var] = left_val // right_val

        # ---------------- PRINT ----------------
        elif parts[0] == 'print':
            var = parts[1]

            if var not in memory:
                raise Exception(f"Runtime Error: Variable '{var}' not declared")

            print(f"FINAL OUTPUT: {memory[var]}")