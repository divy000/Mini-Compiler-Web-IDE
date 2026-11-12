import ply.lex as lex

tokens = (
    'INT', 'IF', 'PRINT',
    'ID', 'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQUALS',
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'SEMICOLON',
    'LT', 'GT'
)

reserved = {
    'int': 'INT',
    'if': 'IF',
    'print': 'PRINT'
}

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_LT = r'<'
t_GT = r'>'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    line = t.value.count('\n') + t.lexer.lexdata.count('\n', 0, t.lexpos) + 1

    last_newline = t.lexer.lexdata.rfind('\n', 0, t.lexpos)
    column = t.lexpos - last_newline

    raise Exception(
        f"Lexical Error at line {line}, column {column}: "
        f"Illegal character '{t.value[0]}'"
    )

lexer = lex.lex()