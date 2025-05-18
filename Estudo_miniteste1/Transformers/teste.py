from lark import Lark, Transformer

grammar = """
    start: bens ":" herds ":" escolhas
    
    bens: bem ( ";" bem )*
    bem: COD "-" DESC "-" valor
    valor: NUM
    DESC: STRING
    
    herds: "(" herd ")" ( "(" herd ")" )*
    herd: COD "," nome "," contacto
    nome: STRING
    contacto: STRING
    
    escolhas: esc+
    esc: COD ">" lst "."
    lst: COD "-" pref ( "," COD "-" pref )*
    pref: "A" | "B" | "C"
    
    COD: /[A-Z0-9]+/
    NUM: /[0-9]+/
    STRING: /".*?"/
    
    %import common.WS
    %ignore WS
"""

class BensTransformer(Transformer):
    def __init__(self):
        self.countHerd = 0
        self.codBens = []

    def start(self, elementos):
        return elementos
    
    def bens(self, bens):
        return bens
    
    def bem(self, bem):
        self.countHerd += 1
        self.codBens.append(bem[0])
    
    def herds(self, args):
        return args
    
    def herd(self, args):
        return args[0]  # Retorna apenas o código do herdeiro

# Criar o parser
partilha_parser = Lark(grammar, start='start', parser='lalr')

# Exemplo de entrada
entrada = '''
B001 - "Carro" - 15000; B002 - "Casa" - 200000:
(H001, "João Silva", "joao@email.com") (H002, "Maria Oliveira", "maria@email.com"):
H001 > B001 - A, B002 - C.
H002 > B002 - A, B001 - B.
'''

# Parsear a entrada e transformar os dados
arvore = partilha_parser.parse(entrada)
transformer = BensTransformer()
nome_herdeiros, lista_bens = transformer.transform(arvore)
print(f"Número de herdeiros: {transformer.countHerd}")
print(f"Lista de bens: {transformer.codBens}")
