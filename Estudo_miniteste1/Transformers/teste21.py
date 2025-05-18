from lark import Lark,Transformer,Discard
from lark.tree import pydot__tree_to_png

grammar = '''
start:"{" elementos "}"
elementos:elemento("," elemento)*
elemento:PAL|NUMERO
PAL:("A".."Z"|"a".."z")+
NUMERO:"0".."9"+
%import common.WS
%ignore WS
'''

input="{10,pal,agora,3,45}"
p = Lark(grammar)
RI = p.parse(input)
print(RI)
print(len(RI.children))
print(RI.children[0])

Tree(Token('RULE', 'start'), [Tree(Token('RULE', 'elementos'), [Tree(Token('RULE', 'elemento'), [Token('NUMERO', '10')]), Tree(Token('RULE', 'elemento'), [Token('PAL', 'pal')]),
     Tree(Token('RULE', 'elemento'), [Token('PAL', 'agora')]), Tree(Token('RULE', 'elemento'), [Token('NUMERO', '3')]), Tree(Token('RULE', 'elemento'), [Token('NUMERO', '45')])])])