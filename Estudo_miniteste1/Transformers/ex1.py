from lark import Lark,Transformer,Discard
from lark.tree import pydot__tree_to_png

grammar1 = '''
// Regras Sintaticas
start: sentido intervalos
sentido: MAIS
       | MENOS
intervalos: intervalo (intervalo)*
intervalo: PE NUM VIR NUM PD

// Regras Lexicográficas
NUM: /-?\d+/
MAIS:"+"
MENOS:"-"
PE:"["
PD:"]"
VIR:","

// Tratamento dos espaços em branco
%import common.WS
%ignore WS
'''

frase = "+ [100,200][300,12]"

p = Lark(grammar1) # cria um objeto parser

tree = p.parse(frase)  # retorna uma tree

#print(tree.pretty())

class TransformerIntervalos(Transformer):
  def __init__(self):
      self.sinal=1
      self.dados = {
            "is_valid": True,
            "first": 0,
            "second": 0,
            "maxrange":0,
        }
  def start(self,elementos):
    print("start",elementos)
    print(f"Amplitude máxima: {self.dados['maxrange']}" )

    return elementos

  def sentido(self,sentido):
    print("sentido",sentido[0].value)
    if sentido[0].value == '-':
      self.sinal=-1
    return Discard

  def intervalos(self,intervalos):
    print("intervalos",intervalos)
    return intervalos

  def intervalo(self,intervalo):
    print("intervalo",intervalo)
    self.dados['first'] = intervalo[0]
    self.dados['second'] = intervalo[-1]
    if (self.sentido == 1 and self.dados['first']  <= self.dados['second']) or (self.sentido == -1 and self.dados['first']  >= self.dados['second']) : 
        self.dados['is_valid'] = True 
    else: 
        self.dados['is_valid'] = False
    if self.dados['maxrange'] <= abs(self.dados['first'] - self.dados['second']):
       self.dados['maxrange'] = abs(self.dados['first'] - self.dados['second'])
    return intervalo

  def NUM (self,numero):
    print("NUM",numero)
    return int(numero)

  def PE(self,pe):
    print("PE",pe)
    return Discard

  def PD(self,pd):
    print("PD",pd)
    return Discard

  def VIR(self,vir):
    print("VIR",vir)
    return vir
  


data = TransformerIntervalos().transform(tree)
print(f"saida :{data}")