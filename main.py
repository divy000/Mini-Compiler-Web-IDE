from parser import parser
from semantic import semantic_analysis
from intermediate import generate_tac
from interpreter import execute_tac

with open("test_program.txt") as f:
    data = f.read()

# Step 1: Parsing
ast = parser.parse(data)
print("\nAST:\n", ast)

# Step 2: Semantic Analysis
print("\nSEMANTIC OUTPUT:\n")
semantic_analysis(ast)

# Step 3: TAC Generation
print("\nTHREE ADDRESS CODE (TAC):\n")
tac = generate_tac(ast)
for line in tac:
    print(line)

# Step 4: Final Execution
print("\nINTERPRETER OUTPUT:\n")
execute_tac(tac)