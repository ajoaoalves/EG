import sys
from TPC1_lex import tokens
import ply.yacc as yacc

def p_Sentence(p): 
    ''' Sentece : Signal Intervals POINT'''

def p_SignalPos(p): 
    ''' Signal : SIGNALPOS'''

def p_SignalNeg(p):
    ''' Signal : SIGNALNEG'''

def p_Intervals(p):
    '''Intervals : Interval RemainingIntervals'''

def p_RemainingIntervals(p):
    ''' RemainingIntervals : 
                           | Interval RemainingIntervals'''

def p_Interval(p):
    ''' Interval : PA NUM COMMA NUM PF '''

parser = yacc.yacc()

while s := input():
   result = parser.parse(s)

#T  = { '.', ';', '[', ']', num }
#NT = { S, Is, RI, I }
#P = { p1: Sentence  : Signal Intervals '.'
#         p6: Signal : '+'
#parser.sentido = 1
#         p7: Signal : '-'		
#parser.sentido = -1
#         p2: Intervals : Interval RemainingIntervals
#         p3: RemainingIntervals : 
#         p4: RemainingIntervals : Interval RemainingIntervals
#         p5: Interval  : '[' num ';' num ']'   
#		CC1:    p[4] > p[2]  &
#		CC2:    p[2] >= parser.anterior
#		parser.anterior = p[4]
#		parser.erro = not (CC1) or not (CC2)