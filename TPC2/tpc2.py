from lark import Lark, Tree
from lark.tree import pydot__tree_to_png

# ------------------------------------------------------------
# TPC1 : Intervalos (definição sintática e verificação simples)
# ------------------------------------------------------------

grammar2 = '''
// Regras Sintáticas
start: signal intervals POINT
signal : MAIS | MENOS
intervals : interval+
interval : PA NUM COMMA NUM PF

// Regras Lexicográficas
MAIS:"+"
MENOS:"-"
PA:"["
PF:"]"
POINT:"."
COMMA: ";" | ","
NUM: /[+-]?\d+/

// Tratamento dos espaços em branco
%import common.WS
%ignore WS
'''

def verificar_ordem(tree):
    """Verifica se todos os números nos intervalos seguem a ordem do sinal."""
    signal = tree.children[0].children[0]  # "+" ou "-"
    all_numbers = []

    for interval in tree.children[1].children:
        nums = [int(child.value) for child in interval.children if child.type == "NUM"]
        all_numbers.extend(nums)

    print(f"Números extraídos: {all_numbers}")

    # Verificar se estão estritamente ordenados
    if signal == "+" and all_numbers != sorted(all_numbers):
        print("Erro: Números fora de ordem para '+'.")
        return "Erro semântico"
    elif signal == "-" and all_numbers != sorted(all_numbers, reverse=True):
        print("Erro: Números fora de ordem para '-'.")
        return "Erro semântico"
    else:
        print("Números ordenados")
        return "Frase correta" 
    
parser = Lark(grammar2, parser="lalr")

inputs = [
    "+ [1;2][3;4][5;6].",  
    "+ [3;1].",  
    "- [5;2][2;0].",  
    "- [5;2][1;3].",
    "- [6;5][6,1]."
]

for frase in inputs:
    print(f"\nVerificando: {frase}")
    try:
        tree = parser.parse(frase)
        print(tree.pretty())  
        resultado = verificar_ordem(tree)
        print(resultado)
    except Exception as e:
        print(f"Erro ao processar entrada: {e}")
