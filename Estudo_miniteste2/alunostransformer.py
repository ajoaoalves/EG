from lark import Lark,Transformer,Discard
from lark.tree import pydot__tree_to_png


grammar = '''
start: (turma LETRA alunos PONTO)+

alunos : aluno (PONTOV aluno)* 

aluno: NOME PE notas PD
notas:  nota (VIR nota)* 

turma : "TURMA"
nota : NUMERO

VIR : ","
PONTOV : ";"
PONTO : "."
LETRA : ("A".."Z")
NOME : ("a".."z")+

NUMERO:"0".."9"+
PE : "("
PD : ")"

%import common.WS
%import common.ESCAPED_STRING
%ignore WS
'''

frase = '''
TURMA A
ana (12, 13, 15, 12, 13, 15, 14);
joao (9,7,3,6,9);
xico (12,16).
TURMA B
rita (15,15,15,18);
ruben (3,18,12);
marta (20,20).
'''
p = Lark(grammar)
tree = p.parse(frase)

class Transformeralunos(Transformer):
    def __init__(self):
        self.numero_alunos = 0
        self.soma_notas = 0
        self.notasorganizadas = {}
        self.notas_do_aluno = {}

    def start(self, tree):

        print(f"Numero de alunos: {self.numero_alunos}")
        print(f"Soma das notas: {self.soma_notas}")
        print(f"Notas por aluno: {self.notasorganizadas}")
        print(f"Notas do aluno: {self.notas_do_aluno}")

        print("start", tree)
        return tree
    
    def turma(self, tree):
        print("turma", tree)
        return Discard
    
    def alunos(self, tree):
        print("alunos", tree)
        return tree
    
    def aluno(self, tree):
        print("aluno", tree)
        self.numero_alunos += 1
        self.notas_do_aluno[tree[0]] = sum(tree[1])/len(tree[1])
        for n in tree[1]:
            print(n)
            if n in self.notasorganizadas.keys():
                self.notasorganizadas[n].add(tree[0])
        return tree
    
    def notas(self, tree):
        print("notas", tree)
        return tree
    
    
    def nota(self, tree):
        print("nota", tree)
        self.soma_notas += int(tree[0])
        if tree[0] not in self.notasorganizadas:
            self.notasorganizadas[tree[0]] = set()
        return int(tree[0])
    
    def PE(self, tree):
        print("PE", tree)
        return Discard
    
    def PD(self, tree):
        print("PD", tree)
        return Discard
    
    def VIR(self, tree):
        print("VIR", tree)
        return Discard
    
    def PONTOV(self, tree):
        print("PONTOV", tree)
        return Discard
    
    def PONTO(self, tree):
        print("PONTO", tree)
        return Discard
    
    def LETRA(self, tree):
        print("LETRA", tree)
        return Discard
    
    def NOME(self, tree):
        print("NOME", tree)
        return tree.value
    
    def NUMERO(self, tree):
        print("NUMERO", tree)
        return int(tree)
    
    
data = Transformeralunos()
data.transform(tree)

