# Mini Compiler with Web IDE

An educational mini compiler built using Python, PLY, and Flask. It supports a simple programming language and provides both a command-line interface and a browser-based IDE.

## Features

- Lexical analysis using PLY
- Syntax analysis and Abstract Syntax Tree (AST) generation
- Semantic analysis and symbol table management
- Three Address Code (TAC) generation
- Execution of generated intermediate code
- Detection of undeclared variables and division by zero
- Browser-based code editor with compiler output

## Supported Language Features

- Integer variable declarations
- Print statements
- Arithmetic operations: `+`, `-`, `*`, `/`
- Parentheses and operator precedence

## Technologies Used

- Python
- Flask
- PLY (Python Lex-Yacc)
- HTML and CSS
- CodeMirror

## Project Structure

```text
compiler_project/
├── app.py
├── lexer.py
├── parser.py
├── semantic.py
├── intermediate.py
├── interpreter.py
├── main.py
├── ui.py
├── test_program.txt
├── requirements.txt
└── README.md
```

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone YOUR_REPOSITORY_URL
   ```

2. Navigate into the project:

   ```bash
   cd compiler_project
   ```

3. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run the Web IDE

```bash
python app.py
```

Open your browser at:

`http://127.0.0.1:5000`

## Run the Command-Line Compiler

```bash
python main.py
```

This executes the sample program in `test_program.txt`.

## Example Program

```c
int a = 5;
int b = 10;
print(a + b * 2);
```

Expected output:

```text
25
```

## Purpose

This project demonstrates the fundamental stages of compiler design, from lexical and syntax analysis to semantic checking, intermediate code generation, and code execution.
