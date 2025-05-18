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

frase = "+ [100,200][3,12]"

p = Lark(grammar1) # cria um objeto parser
tree = p.parse(frase)  # retorna uma tree

#print(tree.pretty())

class TransformerIntervalos(Transformer):
  def __init__(self):
      self.sinal=1
      self.intervalo_correto = False
      self.lista_intervalos = []

  def start(self,elementos):
    print("start",elementos)
    if (self.sinal and self.lista_intervalos == sorted(self.lista_intervalos)) or (self.sinal == -1 and self.lista_intervalos == sorted(self.lista_intervalos,reverse=True)):
      print("Intervalos estão corretos")
    else:
      print("Intervalos estão incorretos")
    return elementos

  def sentido(self,sentido):

    if sentido[0].value == '-':
      self.sinal=-1
    return Discard

  def intervalos(self,intervalos):
    print("intervalos",intervalos)
    return intervalos

  def intervalo(self,intervalo):
    for item in intervalo:
        if isinstance(item, int): 
            self.lista_intervalos.append(item)
    print("intervalo",intervalo)

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
    return vir.value

class calculadora(Transformer):
    def __init__(self):
       self.maioramplitude = 0
       self.intervalo_inicio = 0
       self.intervalo_fim = 0       

    def start(self, items):
        print(f"Maior amplitude: {self.maioramplitude} no intervalo {self.intervalo_inicio } {self.intervalo_fim}")
        return items
 
    def intervalo(self, items):
        print(items)
        inicio = int(items[1])
        fim = int(items[3])
        amplitude = abs(inicio - fim)
        if amplitude > self.maioramplitude:
            self.maioramplitude = amplitude
            self.intervalo_inicio = inicio
            self.intervalo_fim = fim

        return items  


verificador = TransformerIntervalos()
verificador.transform(tree)

amplitude_calc = calculadora()
amplitude_calc.transform(tree)
