from lark import Discard
from lark import Lark,Token,Tree
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter

class listainterpreter(Interpreter):
    def __init__ (self):
        self.comprimento = 0
        self.maisrepetido = 0
        self.soma = 0
        self.ocorrencias = {}
        self.flag = 0

    def start(self, tree):
        r = self.visit(tree.children[1])
        print("Comprimento:", self.comprimento)
        print("Soma:", self.soma)
        print("Ocorrencias:", self.ocorrencias)
        print("Max ocorrencias:", max(self.ocorrencias, key=self.ocorrencias.get))
        return (self.comprimento, self.maisrepetido, self.soma, self.ocorrencias, r)

    def elementos(self, tree):
        r = self.visit_children(tree)

        return r
    
    def elemento(self, tree):
        r = self.visit_children(tree)
        print(tree.children[0])
        self.comprimento += 1

        if (r[0].type == 'NUM'):   
            if r[0] in self.ocorrencias:
                self.ocorrencias[int(r[0])] += 1
            else:
                self.ocorrencias[int(r[0])] = 1
            if self.flag > 0:
                self.soma += int(r[0])
            return int(r[0])
        if (r[0] == 'agora'):
            self.flag += 1
            return "agora"
        if (r[0] == 'fim'):
            self.flag -= 1
            return "fim"
        
    def LISTA(self, args):
        return Discard
    
    def PONTO(self, args):
        return Discard
    
    def VIR(self, args):
        return Discard
    
    def NUM(self, args):
        return int(args)
    
    def PALAV(self, args):
        return str(args)
            

grammar1 = '''
// Regras Sintaticas
start: LISTA elementos PONTO
elementos: elemento (VIR elemento)*

elemento: NUM | PALAV

// Regras Lexicográficas
LISTA: "Lista"i  
PONTO:  "."
VIR : ","
NUM: /\d+/
PALAV: /[a-zA-Z_][a-zA-Z0-9_]*/

// Tratamento dos espaços em branco
%import common.WS
%ignore WS
'''

frase = "Lista 1 ,agora, 1 ,agora, 3, fim, 4, fim ,5 ,agora, 6,fim. "

p = Lark(grammar1) # cria um objeto parser
tree = p.parse(frase)  # retorna uma tree

data = listainterpreter().visit(tree)