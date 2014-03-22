import sys,math
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

tokens = (
    'NAME','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS','MOD','LOG','SQRT','POW','SIN','COS','TAN','FAC'

    )

literals = ['=','+','-','*','/', '(',')','%','^']

# Tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_MOD     = r'\%'

def t_FAC(t):
    r'fac'
    #print t
    return t

def t_TAN(t):
    r'tan'
    #print t
    return t
def t_COS(t):
    r'cos'
    #print t
    return t
def t_SIN(t):
    r'sin'
    #print t
    return t
def t_POW(t):
    r'\^'
    #print t
    return t
def t_LOG(t):
    r'log'
    #print t
    return t
def t_SQRT(t):
    r'sqrt'
    #print t
    return t

def t_COMMENT(t):
    r'\#.*'
    #print t
    pass
    
def t_NUMBER(t):
    r'[\d+][.][\d+]| \d+'
#    r'\d+'
    t.value = float(t.value)
    #print t
    return t

 
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    #print t
    return t


t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lex.lex()

# Parsing rules

precedence = (
    ('left','LOG','SQRT','POW','SIN','COS','TAN','FAC'),
    ('left','PLUS','MINUS','MOD'),
    ('left','TIMES','DIVIDE'),

    ('right','UMINUS'),
    )

# dictionary of names
names = { }

def p_statement_assign(p):
    'statement : NAME EQUALS expression'
    names[p[1]] = p[3]

def p_statement_expr(p):
    'statement : expression'
    print(p[1])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MOD expression'''
    if p[2] == '+'  : p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]
    elif p[2] == '%': p[0] = p[1] % p[3]

def p_expression_uminus(p):
    "expression : MINUS expression %prec UMINUS"
    p[0] = -p[2]

def p_expression_trigonometric(p):
    '''expression : COS expression
                  | TAN expression
                  | SIN expression'''
    if p[1]=='cos'  :p[0] = math.cos(p[2])
    elif p[1]=='tan':p[0] = math.tan(p[2])
    elif p[1]=='sin':p[0] = math.sin(p[2])


def p_expression_pow(p):
    "expression : expression POW expression "
    p[0] = math.pow(p[1],p[3])

def p_expression_fac(p):
    "expression : FAC expression "
    p[0] = math.factorial(p[2])

def p_expression_log(p):
    "expression : LOG expression "
    p[0] = math.log10(p[2])

def p_expression_sqrt(p):
    "expression : SQRT expression "
    p[0] = math.sqrt(p[2])

def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]

def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
yacc.yacc()

while 1:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break
    if not s: continue
    yacc.parse(s)
