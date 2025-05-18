#Exercício 2
#
#Desenvolva uma GIC para definir uma linguagem que permita escrever listas mistas de números e palavras, de tal forma que as 3 frases abaixo sejam frases válidas dessa linguagem:
#
#LISTA 1 .
#
#Lista aaa .
#
#Lista 1, 2, agora, 3, 4, fim, 7, 8.
#
#Resolva as seguintes alíneas recorrendo ao uso de Transformer :
#
#(a) Calcule, retorne e imprima quantos elementos existem numa lista.
#
#(b) Identifique, retorne e imprima o elemento que mais se repete numa lista.
#
#(c) Calcule, retorne e imprima a soma de todos os números que se encontrem entre as palavras agora e fim de uma lista.
#
#(d) Verifique se uma lista é válida de acordo com os seguintes parâmetros :

from lark import Lark,Transformer,Discard
from lark.tree import pydot__tree_to_png
from collections import Counter

grammar1 = R'''
// Regras SIntáticas
start: LIST conteudo PONTO
conteudo : elem (COMMA elem)*
elem : STRING
     | NUM

// Regras Lexicográficas
COMMA: ","
PONTO: "."
LIST: "Lista"i  // O "i" no final torna case-insensitive
NUM: /\d+/
STRING: /[a-zA-Z_][a-zA-Z0-9_]*/

// Tratamento dos espaços em branco
%import common.WS
%ignore WS
'''

frase1 = "Lista 1, 2, agora, 3, 4, fim, 7, 8."
frase2 = "Lista 1, 2, 3, 4, fim, 7, 8."
frase3 =  "Lista 1, inicio, 2, 3, 4, fim, 7, 8, inicio."
frase4 = "Lista 1, 2, 3, inicio, fim, 7, 8."
frase5 = "Lista 1, agora, 2, agora, 3, fim, 4, fim, 5, 6, agora, 10, fim."


p = Lark(grammar1)

tree = p.parse(frase5)

print(tree.pretty())

class TransformerValid(Transformer):
    def __init__(self):
        self.error = False
        self.listaelementos = []
        self.estado = False
        self.contaagora = 0 #Verifica se antes do fim tem um agora 
        self.contafim = 0
        self.contaelem = 0

    def start(self, elementos):
        #print("start", elementos)
        return elementos
    def conteudo(self,conteudo):
        #print("AQUI conteudo", conteudo)
        for elem in self.listaelementos:
            if elem == "agora":
                self.estado = True
                self.contaagora +=1
            if elem == "fim":
                if (self.contaelem == 0 and self.estado == True) :
                    self.error = True
                self.estado = False
                self.contafim +=1
                self.contaelem = 0
            elif self.estado == True:
                 self.contaelem += 1
        if (self.estado == True or (self.contafim > 0 and self.contaagora == 0)):
            self.error = True  # Define erro
            print("ERRO: 'agora' e 'fim' não aparecem corretamente!")
        return conteudo
    
    def elem (self,elem):
        self.listaelementos.append(str(elem[0]))
        #print("elem", elem)
        return elem
    def PONTO(sef, ponto):
        #print("PONTO", ponto)
        return Discard
    def LISTA(self, lista):
        #print("LISTA", lista)
        return Discard
    def NUM(self, num):
        #print("NUM", num)
        return num
    def STRING(self, string):
        #print("STRING", string)
        return string
    
valid_transformer = TransformerValid()
valid_transformer.transform(tree)

if valid_transformer.error:
    print("Erro: A lista não está correta.")
else:
    print("A lista está correta.")

    class TransformerCalculate:
        def __init__(self, lista_validada):
            self.listaelementos = lista_validada  # Usa a lista validada
            self.tamanho_lista = 0
            self.maisRepetido = None
            self.soma = 0
            self.agora = False

        def calcular_tamanho(self):
            self.tamanho_lista = len(self.listaelementos)
            print(f"Tamanho da lista: {self.tamanho_lista}")
            return self.tamanho_lista

        def mais_Repetido(self):
            if not self.listaelementos:
                return None
            contador = Counter(self.listaelementos)
            self.mais_repetido = contador.most_common(1)[0]
            print(self.mais_repetido)
            return self.mais_repetido

        def calcular_soma(self):
            for elem in self.listaelementos:
                if elem == "agora":
                    self.agora = True
                if elem == "fim":
                    self.agora = False
                elif elem.isdigit() and self.agora == True:
                    self.soma += int(elem)
            print(self.soma)
            return self.soma


    calc_transformer = TransformerCalculate(valid_transformer.listaelementos)
    
    calc_transformer.calcular_tamanho()  # Calcula o tamanho da lista
    calc_transformer.mais_Repetido()  # Encontra o elemento mais repetido
    calc_transformer.calcular_soma()  # Soma os números entre 'agora' e 'fim'