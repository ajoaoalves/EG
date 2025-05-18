from lark import Lark, Tree
from lark.tree import pydot__tree_to_png

SA(start) {}
SA(intervals) {anterioro : int}
IA(intervals) {sentido : bool, anteriori: int}
SA(interval) {maior:int}
IA (interval) {sentido:bool}

grammar = '''
//regras sintaticas

'''