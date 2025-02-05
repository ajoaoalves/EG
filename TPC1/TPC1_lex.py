import re
import ply.lex as lex

tokens = ('MENOS',
          'MAIS',
          'PA',
          'PF',
          'COMMA',
          'POINT',
          'NUM')

t_MAIS = r'\+'
t_MENOS = r'\-'
t_PA = r'\['
t_PF = r'\]'
t_COMMA = r'[;,]'
t_POINT = r'\.'

def t_NUM(t):
    r'([-+]?\d+)'  
    t.value = int(t.value)  
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
