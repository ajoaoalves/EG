import re
import ply.lex as lex

tokens = ('SIGNALPOS',
          'SIGNALNEG',
          'PA',
          'PF',
          'COMMA',
          'POINT',
          'NUM')

t_SIGNALPOS = r'\+'
t_SIGNALNEG = r'\-'
t_PA = r'\['
t_PF = r'\]'
t_COMMA = r';'
t_POINT = r'\.'

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Give the lexer some input
while True:
    data = input("Enter data: ")
    if data == "STOP":
        break
    lexer.input(data)
    for tok in lexer:
        if tok.type == "NUM":
            print("variavel", tok.value)
        if tok.type == "PA" or tok.type == "PF" or tok.type == "COMMA" or tok.type == "POINT" or tok.type == "SIGNALPOS" or tok.type == "SIGNALNEG" :
            print("operador encontrado")
        elif tok.type == "NEWLINE":
            print("\n")
        #print(tok.type, tok.value, tok.lineno, tok.lexpos)