import ply.yacc as yacc
from lexer import tokens

# ---------------- PROGRAM ----------------
def p_program(p):
    '''program : statements'''
    p[0] = p[1]

# ---------------- STATEMENTS ----------------
def p_statements_multiple(p):
    '''statements : statement statements'''
    p[0] = [p[1]] + p[2]

def p_statements_single(p):
    '''statements : statement'''
    p[0] = [p[1]]

# ---------------- STATEMENTS ----------------
def p_statement_declare(p):
    '''statement : INT ID EQUALS expression SEMICOLON'''
    p[0] = ('declare', p[2], p[4])

def p_statement_print(p):
    '''statement : PRINT LPAREN expression RPAREN SEMICOLON'''
    p[0] = ('print', p[3])

# ---------------- EXPRESSIONS ----------------
def p_expression_plus(p):
    '''expression : expression PLUS term'''
    p[0] = ('+', p[1], p[3])

def p_expression_minus(p):
    '''expression : expression MINUS term'''
    p[0] = ('-', p[1], p[3])

def p_expression_term(p):
    '''expression : term'''
    p[0] = p[1]

# ---------------- TERMS ----------------
def p_term_times(p):
    '''term : term TIMES factor'''
    p[0] = ('*', p[1], p[3])

def p_term_div(p):
    '''term : term DIVIDE factor'''
    p[0] = ('/', p[1], p[3])

def p_term_factor(p):
    '''term : factor'''
    p[0] = p[1]

# ---------------- FACTORS ----------------
def p_factor_number(p):
    '''factor : NUMBER'''
    p[0] = p[1]

def p_factor_id(p):
    '''factor : ID'''
    p[0] = ('var', p[1])

def p_factor_expr(p):
    '''factor : LPAREN expression RPAREN'''
    p[0] = p[2]

# ---------------- ERROR ----------------
def p_error(p):
    if p:
        raise Exception(f"Syntax Error near '{p.value}'")
    else:
        raise Exception("Syntax Error at EOF")

parser = yacc.yacc()