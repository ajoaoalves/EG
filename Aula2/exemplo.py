from lark import Lark
from lark.tree import pydot__tree_to_png

grammar2 = '''
// Regras Sintaticas
start: PE ( | elementos) PD
elementos : elemento (VIR elemento)*
elemento : NUMERO

// Regras Lexicográficas
NUMERO:"0".."9"+ // [0-9]+
PE:"["
PD:"]"
VIR:","

// Tratamento dos espaços em branco
%import common.WS
%ignore WS
'''

frase = "[1,23,345]"

p = Lark(grammar2) # cria um objeto parser

tree = p.parse(frase)  # retorna uma tree
print(tree)
print(tree.pretty())
pydot__tree_to_png(tree,'lark_test.png')