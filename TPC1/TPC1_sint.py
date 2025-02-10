import sys
from TPC1_lex import tokens
import ply.yacc as yacc

# ------------------------------------------------------------
# TPC1 : Intervalos (definição sintática)
#  + [1,2][3,4][5,6].
#  + [100,200][3,12].
#  + [-4,-2][10,100].
#  - [19,15][12,6][-1,-3].
#  - [1000,200][30,12].
# ------------------------------------------------------------

def p_Sentence_1(p): 
    ''' Sentence : MENOS Intervals POINT'''
    intervals_aux = p[2]
    max = len(intervals_aux)

    if max == 1 and (intervals_aux[0][0] - intervals_aux[0][1] >= 0): 
            print(f"Intervalos Ordenados")

    for i in range(len(intervals_aux) - 1): 
        if ((intervals_aux[i][0] - intervals_aux[i][1] >= 0 and intervals_aux[i+1][0] - intervals_aux[i][1] <= 0) and (intervals_aux[max-1][0] - intervals_aux[max-1][1] >= 0)):
            print(f"Intervalos Ordenados")
        else:
            print(f"Intervalos desordenados")
            break  

def p_Sentence_2(p): 
    ''' Sentence : MAIS Intervals POINT'''
    intervals_aux = p[2]
    max = len(intervals_aux)

    if (max == 1 and (intervals_aux[0][1] - intervals_aux[0][0] >= 0)): 
        print(f"Intervalos Ordenados")

    for i in range(len(intervals_aux) - 1): 
        
        if (max > 1 and ((intervals_aux[i][0] - intervals_aux[i][1] <= 0 and  intervals_aux[i][1] - intervals_aux[i+1][0] <= 0) and (intervals_aux[max-1][0] - intervals_aux[max-1][1] <= 0))):
            print(f"Intervalos Ordenados")
        else:
            print(f"Intervalos desordenados")
            break  

def p_SignalPos(p): 
    ''' Signal : '+' '''
    p[0] = p[1]

def p_SignalNeg(p):
    ''' Signal : '-' '''
    p[0] = p[1]

def p_Intervals(p):
    '''Intervals : Interval RemainingIntervals'''
    p[0] = [p[1]] + p[2]
    

def p_RemainingIntervals(p):
    ''' RemainingIntervals : 
                           | Interval RemainingIntervals'''
    if len(p) > 1:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_Interval(p):
    ''' Interval : PA NUM COMMA NUM PF '''
    p[0] = [p[2], p[4]]  

def p_error(p):
    print("Erro sintático no input!")
    if p:
        print(f"Erro próximo ao token {p.value}")

parser = yacc.yacc()

while True:
    s = input("Insira Input (ou 's' para sair): ")
    if s.lower() == 's':
        break
    result = parser.parse(s)
