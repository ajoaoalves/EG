from lark import Discard
from lark import Lark,Token,Tree
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter

class MyInterpreter(Interpreter):
    def __init__(self):
        self.numeroalunos = 0
        self.numeronotas = 0
        self.soma = 0
        self.media = 0
        self.mediaalunos = {}

    def start(self, tree):
        r = self.visit(tree.children[2])
        self.media = self.soma / self.numeronotas if self.numeronotas > 0 else 0
        print("Número de alunos:", self.numeroalunos)
        print("Soma das notas:", self.soma)
        print("Média das notas:", self.media)
        return r,self.numeroalunos, self.soma, self.media, self.numeronotas, self.mediaalunos
        

    def alunos(self,tree):
        r = self.visit_children(tree)
        return r

    def aluno(self, tree):
        nome = tree.children[0].value 
        notas = []

        for elemento in tree.children[2].children:
            if isinstance(elemento, Tree) and elemento.data == 'nota':
                nota = self.visit(elemento)
                notas.append(nota)
                self.numeronotas += 1
                self.soma += nota

        media = sum(notas) / len(notas) if notas else 0
        self.mediaalunos[nome] = media
        self.numeroalunos += 1
        print(f"{nome}: notas={notas}, média={media:.2f}")
        return notas



    def notas(self, tree):
        r = self.visit_children(tree)
        r = 0
        print(tree.children)
        for elemento in tree.children:
            if elemento.data == 'nota' and isinstance(elemento, Tree):
                r += self.visit(elemento)

        return r
        
    def turma(self, tree):
        return Discard

    def nota(self, tree):
        r = self.visit_children(tree)
        if r[0].type == 'NUMERO':
            self.numeronotas += 1
            self.soma += int(r[0])
            return int(r[0])
        else:
            return 0
        
    def PE(self, token):
        return Discard

    def PD(self, token):
        return Discard

    def VIR(self, token):
        return Discard

    def PONTOV(self, token):
        return Discard

    def PONTO(self, token):
        return Discard

    def LETRA(self, token):
        return Discard

    def NOME(self, token):
        return token.value
    

grammar = '''
start: turma LETRA alunos PONTO

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
'''
p = Lark(grammar)
parse_tree = p.parse(frase)

data = MyInterpreter().visit(parse_tree)
