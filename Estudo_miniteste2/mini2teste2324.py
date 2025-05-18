from lark import Discard
from lark import Lark,Token,Tree
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter

class MyInterpreter(Interpreter):
    def __init__(self):
        self.horapartida = []
        self.horachegada = []
        self.id = []
        self.companhias = {}
        self.flagpartidas = True

    def start(self, tree):
        r = self.visit_children(tree)
        print("horas partidas", self.horapartida)
        print("horas chegadas", self.horachegada)
        return (self.horapartida, self.horachegada,self.ids,self.companhias,r)
    
    def trafego(self, tree):
        r = self.visit_children(tree)
        return r
    
    def partidas(self, tree):
        self.flagpartidas = True

        r = self.visit_children(tree)

        
        return r
    
    def chegadas(self, tree):
        self.flagpartidas = False

        r = self.visit_children(tree)

        return r
    
    def aviao(self, tree):
        r = self.visit_children(tree)
        hora = int(tree.children[3])
        self.id.append(tree.children[0])
        companhia = tree.children[1].strip('"')
        if self.flagpartidas:
            self.horapartida.append(hora)
        else:
            self.horachegada.append(hora)
        if companhia not in self.companhias:
            self.companhias[companhia] = 1
        else:
            self.companhias[companhia] += 1
        return r 
        
        
    def NUMVOO(self, token):
        return token.value

    def COMPANH(self, token):
        return token.value[1:-1]  # Remove aspas

    def ORIGDEST(self, token):
        return token.value[1:-1]  # Remove aspas
    
    def DATA(self, token):
        return token.value
    
    def HORA(self, token):
        return int(token.value)
    

grammar = """
start: trafego

trafego: DATA partidas chegadas

partidas: "partidas" aviao*
chegadas: "chegadas" aviao*

aviao: NUMVOO "-" COMPANH "-" ORIGDEST ":" HORA

NUMVOO: ID 
COMPANH: STR 
ORIGDEST: STR 


DATA: /[\d-]+/    # Formato de data
ID: /[A-Za-z]+/   # Identificador
STR: /"[^"]*"/     # String entre aspas
HORA: /\d+/        # Hora (ex: 1200)

// Ignorar espaços em branco
%import common.WS
%import common.ESCAPED_STRING
%ignore WS
"""

frase = '''
2023-10-05 
partidas 
    AB - "XYZ" - "Aeroporto1" : 1000 
    dsfbB - "XYZ" - "Aeroporto1" : 1000 

chegadas 
    CD - "ABC" - "Aeroporto2" : 1200 
    dsffsbB - "SDA" - "Aeroporto1" : 1000 



'''

p = Lark(grammar)
parse_tree = p.parse(frase)

data = MyInterpreter().visit(parse_tree)

horas_partida = data[0]
horas_chegada = data[1]
ids = data[2]
companhias = data[3]
print("Companhias:", companhias)



for i in range(len(horas_partida)):
    if len(horas_partida) != len(horas_chegada):
        print("Erro: Número de partidas e chegadas não coincide")
        break
    if horas_partida[i] > horas_chegada[i]:
        print(f"Erro: Hora de partida {horas_partida[i]} é maior que hora de chegada {horas_chegada[i]} para o voo {ids[i]}")