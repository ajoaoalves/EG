from lark import Lark,Transformer,Discard
from lark.tree import pydot__tree_to_png

grammar = '''
start : partilhas
partilhas : bens ";" herds ":" escolhas
bens : bem ( ";" bens )*
herds : "(" herd ")" ( "(" herd ")" )*
escolhas : esc+
esc : cod ">" lst "."
lst : cod "-" pref ( "," cod "-" pref )*
pref : A | B | C
bem : cod "-" desc "-" valor
herd : cod "," nome "," contacto
nome : STR
contacto : NUM
cod : STR
valor : NUM
desc : STR

A : "A"i
B : "B"i
C : "C"i
STR: ESCAPED_STRING
NUM : SIGNED_NUMBER

// Tratamento dos espaços em branco
%import common.WS
%import common.ESCAPED_STRING
%import common.SIGNED_NUMBER
%ignore WS

'''

frase = ''' "Ba" - "Casa de Praia" - 15 ; "Bb" - "Carro Familiar" - 20 ; ( "Ha" , "Maria Silva" , 912345678 ) ( "Hb" , "João Pereira" , 934567890 ) : 
"Ea" > "Ha" - A , "Hb" - B .
"Eb" > "Hb" - C , "Ha" - A . 
'''

p = Lark(grammar) # cria um objeto parser
tree = p.parse(frase)  # retorna uma tree

class MyTransformer(Transformer):
    def __init__(self):
        self.numeroherdeiros = 0
        self.listacodigos = []

    def start(self, args):
        print("start",args)
        return args
    
    def partilhas(self, args):
        print("partilhas",args)
        return args
    
    def bens(self, args):
        print("bens",args)
        return args
    
    def herds(self, args):
        print("herds",args)
        return args
    
    def escolhas(self, args):
        print("escolhas",args)
        return args
    
    def esc(self, args):
        print("esc",args)
        return args
    
    def lst(self, args):
        print("lst",args)
        return args
    
    def pref(self, args):
        print("pref",args)
        return args
    
    def bem(self, args):
        print("bem",args[0])
        self.listacodigos.append(str(args[0]))
        return args
    
    def valor(self, args):
        print("valor",args)
        return int(args[0])
    
    def cod (self, args):
        print("cod",args)
        return str(args[0])
    
    def desc(self, args):
        print("desc",args)
        return str(args[1:-1])
    
    def herd(self, args):
        print("herd",args)
        self.numeroherdeiros += 1
        return args
    
    def nome(self, args):
        print("nome",args)
        return str(args[1:-1])
    
    def contacto(self, args):
        print("contacto",args)
        return int(args[0])
    
data = MyTransformer()
data.transform(tree)

print("Número de herdeiros:", data.numeroherdeiros)
print("Lista de códigos:", data.listacodigos)