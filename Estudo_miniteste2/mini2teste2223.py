from lark import Discard
from lark import Lark,Token,Tree
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter

class MyInterpreter(Interpreter):
    def __init__(self):
        self.movimentosdebito = 0
        self.movimentoscredito = 0
        self.valortotal = 0
        self.listadestino = []

    def start(self, tree):
        r = self.visit_children(tree)
        return (self.movimentosdebito, self.movimentoscredito, self.valortotal,self.listadestino, r)
    
    def transacoes(self,tree):
        r = self.visit_children(tree)
        return r

    def movimentos(self, tree):
        r = self.visit_children(tree)
        return r
    
    def move (self, tree):
        r = self.visit_children(tree)

        return r 
    
    def cntdestino (self,tree):
        r = self.visit_children(tree)
        contadestino = str(tree.children[0])
        self.listadestino.append(contadestino)

        return r
    
    def sinal (self, tree):
        r = self.visit_children(tree)
        if tree.children[0] == 'credito':
            self.movimentoscredito += 1
        else:
            self.movimentosdebito += 1
        return r
    
    def quantia (self, tree):
        r = self.visit_children(tree)
        self.valortotal += int(tree.children[0])
        return r
    
    def cntordenante (self, tree):
        r = self.visit_children(tree)
        return r
    
    def descr(self, tree):
        r = self.visit_children(tree)
        return r
    
    def data(self, tree):
        r = self.visit_children(tree)
        return r
    
    def CREDITO(self, token):
        return str(token.value)
    
    def DEBITO(self, token):
        return str(token.value)

    def ID(self, token):
        return str(token.value.strip(""))
    
    def STR(self, token):
        return str(token.value.strip(""))
    
    def NUM(self, token):
        return int(token.value)

grammar = """
start: transacoes
transacoes : BTASK movimentos ETASK
movimentos : move "."
           | movimentos move "."
move : data ";" cntdestino ";" sinal ";" quantia ";" cntordenante ";" descr
cntdestino : ID
sinal : CREDITO 
      | DEBITO
quantia : NUM
cntordenante : ID
descr : STR
data : STR

BTASK : "btask"i
ETASK : "etask"i
CREDITO : "credito"i
DEBITO : "debito"i
ID: /[A-Za-z]+/   
STR: /"[^"]*"/ 
NUM : /\d+/

%import common.WS  # <-- Adicione estas linhas
%import common.ESCAPED_STRING
%ignore WS         # <-- para ignorar espaços
"""
frase = '''BTASK "2023-10-05" ; ContaPoupanca ; credito ; 15 ; ClienteAna ; "Depósito salarial" . "2023-09-30" ; Supermercado ; debito ; 30 ; CartaoMaria ; "Compras mensais" . "2023-10-01" ; Netflix ; debito ; 20 ; CartaoJoao ; "Assinatura streaming" . ETASK'''
p = Lark(grammar)
parse_tree = p.parse(frase)

data = MyInterpreter().visit(parse_tree)

print("Número de movimentos de débito: ",data[0])
print("Número de movimentos de crédito: ",data[1])
print("Valor total: ",data[2])
print("Lista de destinos: ",data[3])
