from lark import Lark, Token, Tree
from lark.visitors import Interpreter

class MyInterpreter(Interpreter):
    def __init__(self):
        self.contaAlunos = 0
        self.somaNotas = 0
        self.Testes = {}  
        self.NotasPorAlunos = {} 

    def start(self, tree):
        self.visit_children(tree)

        print("\nNotas associadas a alunos:")
        for nota, alunos in self.NotasPorAlunos.items():
            print(f"{nota}: {alunos}")

        return self.contaAlunos, self.somaNotas, self.Testes, self.NotasPorAlunos

    def turma(self, tree):
        for aluno in tree.children:
            if isinstance(aluno, Tree) and aluno.data == "aluno":
                self.contaAlunos += 1
                self.visit(aluno)

    def aluno(self, tree):
        nome_aluno = tree.children[0].value 
        notas = []  

        for elem in tree.children:
            if isinstance(elem, Tree) and elem.data == "notas":
                for nota in elem.children:
                    if isinstance(nota, Token) and nota.type == "NOTA":
                        valor = int(nota.value)
                        notas.append(valor)  
                        self.somaNotas += valor  

                        if valor not in self.NotasPorAlunos:
                            self.NotasPorAlunos[valor] = set()
                        self.NotasPorAlunos[valor].add(nome_aluno)

        self.Testes[nome_aluno] = notas 

## Gramatica

grammar = '''
start: turma+
turma: "TURMA" LETRA (aluno)+ "."
aluno: NOME notas
notas: PE NOTA ("," NOTA)* PD 
NOME: ("A".."Z"|"a".."z")+
LETRA: ("A".."Z")
NOTA: ("0".."9")+
PE: "("
PD: ")"

%import common.WS
%ignore WS
'''

frase = '''TURMA A
ana (12, 13, 15, 12, 13, 15, 14)
joao (9, 7, 3, 6, 9, 12)
xico (12, 16).'''

p = Lark(grammar)
parse_tree = p.parse(frase)

data = MyInterpreter().visit(parse_tree)

print("\nNúmero de alunos:", data[0])
print("Notas por aluno:", data[2])
print("Notas organizadas:", data[3]) 