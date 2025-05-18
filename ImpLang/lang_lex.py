import ply.lex as lex

tokens = (
    'IF', 'THEN', 'WHILE', 'DO', 'FROM', 'TO',
    'IDENTIFIER', 'TYPE_INT', 'INT', 'TYPE_STRING', 'STRING',
    'TYPE_SET', 'SET', 'TYPE_ARRAY', 'ARRAY', 
    'EQUAL', 'OPERATOR', 'REL_OP', 'LOG_OP',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON',
    'RETURN','FUNC','ROW'
)

reserved = {
    'int': 'TYPE_INT',
    'string': 'TYPE_STRING',
    'set': 'TYPE_SET',
    'array': 'TYPE_ARRAY',
    'IF': 'IF',
    'THEN': 'THEN',
    'WHILE': 'WHILE',
    'DO': 'DO',
    'FROM': 'FROM',
    'TO': 'TO',
    'RETURN':'RETURN',
    'FUNC':'FUNC',
    'ROW':'ROW'
}

t_EQUAL    = r'='
t_OPERATOR = r'[\+\-\*/%^]'
t_REL_OP   = r'==|!=|<|>|<=|>='
t_LOG_OP   = r'AND|OR'
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_LBRACE   = r'\{'
t_RBRACE   = r'\}'
t_SEMICOLON = r';'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\".*?\"|\'.*?\''
    t.value = t.value[1:-1]  # Remove as aspas
    return t

def t_SET(t):
    r'\{(\s*\d+\s*(,\s*\d+\s*)*)?\}'
    t.value = eval(t.value)  # Converte a string para um conjunto
    return t

def t_ARRAY(t):
    r'\[(\s*\d+\s*(,\s*\d+\s*)*)?\]'
    t.value = eval(t.value)  # Converte a string para uma lista
    return t


t_ignore = ' \t'

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractere inválido: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()
#
#codigo_exemplo1 = """
#int x = 10;
#string nome = "João";
#set A = {1, 2, 3};
#array nums = [10, 20, 30];
#
#IF (x > 10) THEN y = y + 1;

#IF (x > 10) THEN {
#             y = y+1;
#             WHILE (x < 100) DO x = x * 2; 
#}
#WHILE (x < 100) DO x = x * 2;
#FROM i = 1 TO 10 DO x = x + i;
#"""
#
#print("\nTokens extraídos:")
#lexer.input(codigo_exemplo1)
#for tok in lexer:
#    print(tok)
#