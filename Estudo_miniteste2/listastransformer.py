from lark import Lark,Transformer,Discard
from lark.tree import pydot__tree_to_png

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

frase = "Lista 1 ,agora, 2 ,agora, 3, fim, 4, fim ,5 ,agora, 6,fim. "

p = Lark(grammar1) # cria um objeto parser
tree = p.parse(frase)  # retorna uma tree

class ValidaLista(Transformer):
    def __init__(self):
        self.stack = []  # pilha para armazenar contadores entre 'agora' e 'fim'
        self.erros = []


    def start(self, args):
        print("start",args)
        return args
    
    def elementos(self, args):
        print("elementos",args)
        return args
    
    def elemento(self, args):
        valor = args[0]
        if valor == "agora":
            self.stack.append(0)  # inicia contador de números neste bloco
        elif valor == "fim":
            if not self.stack:
                self.erros.append("Erro: 'fim' sem 'agora'")
            else:
                count = self.stack.pop() #remove e retorna o último elemento
                if count == 0:
                    self.erros.append("Erro: Nenhum número entre 'agora' e 'fim'")
        elif isinstance(valor, int):
            if self.stack:
                self.stack[-1] += 1  # incrementa o contador no bloco atual
        return args

    
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
    
valida = ValidaLista()
valida.transform(tree)

for erro in valida.erros:
    print(erro)  

class ListaTransformer(Transformer):
    def __init__(self):
        self.tamanholista = 0
        self.soma = 0
        self.ocorrencias  = {}
        self.in_contagem = 0

    def start(self, args):
        return args
    
    def elementos(self, args):
        return args
    
    def elemento(self, args):
        if args[0] == "agora":
            self.in_contagem += 1   
        if  args[0] == "fim":
            self.in_contagem -= 1 
        if isinstance(args[0], int) and self.in_contagem > 0:
                    self.soma += int(args[0])
        if args[0] in self.ocorrencias:
            self.ocorrencias[args[0]] += 1
        else:
            self.ocorrencias[args[0]] = 1
        self.tamanholista += 1
        return args

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
    
calcula = ListaTransformer()
calcula.transform(tree)

print("Tamanho da lista:", calcula.tamanholista)
print("Soma dos elementos:", calcula.soma)
print("Ocorrências de cada elemento:", calcula.ocorrencias)
print("Elemento com mais ocorrências:", max(calcula.ocorrencias, key=calcula.ocorrencias.get))