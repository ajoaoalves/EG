import ply.yacc as yacc
from lang_lex import tokens  
symbol_table = {}

def p_annotation(p):
    '''annotation : inputs ROW outputs FUNC IDENTIFIER LBRACE body RBRACE'''
    pass

def p_inputs(p):
    '''inputs : input
              | input inputs'''
    pass

def p_input(p):
    '''input : TYPE_INT IDENTIFIER
             | TYPE_STRING IDENTIFIER
             | TYPE_SET IDENTIFIER
             | TYPE_ARRAY IDENTIFIER'''
    if p[2] in symbol_table:
        print(f"Erro semântico: Variável '{p[2]}' já foi declarada.")
    else:
        symbol_table[p[2]] = p[1]

def p_outputs(p):
    '''outputs : RETURN output
               | RETURN output outputs'''
    pass

def p_output(p):
    '''output : TYPE_INT IDENTIFIER
              | TYPE_STRING IDENTIFIER
              | TYPE_SET IDENTIFIER
              | TYPE_ARRAY IDENTIFIER'''
    if p[2] in symbol_table:
        print(f"Erro semântico: Variável de saída '{p[2]}' já foi declarada.")
    else:
        symbol_table[p[2]] = p[1]

def p_body(p):
    '''body : statement
            | statement body'''
    pass

def p_statement(p):
    '''statement : selection
                 | repetition
                 | assignment'''
    pass

def p_selection(p):
    '''selection : IF LPAREN condition RPAREN THEN action'''
    pass

def p_repetition(p):
    '''repetition : WHILE LPAREN condition RPAREN DO action
                  | FROM IDENTIFIER EQUAL INT TO INT DO action'''
                  
    if p[2] not in symbol_table:
        print(f"Erro semântico: Variável '{p[2]}' não foi declarada antes do loop.")

def p_condition(p):
    '''condition : comparison'''
    pass

def p_comparison(p):
    '''comparison : expression REL_OP expression
                  | comparison LOG_OP comparison'''

def p_expression(p):
    '''expression : IDENTIFIER
                  | INT
                  | STRING
                  | LPAREN expression RPAREN
                  | expression OPERATOR expression'''
    if len(p) == 2:
        if isinstance(p[1], str) and p[1] not in symbol_table:
            print(f"Erro semântico: Variável '{p[1]}' não foi declarada.")
    elif len(p) == 4:
        left, op, right = p[1], p[2], p[3]
        left_type = symbol_table.get(left, 'TYPE_INT' if isinstance(left, int) else None)
        right_type = symbol_table.get(right, 'TYPE_INT' if isinstance(right, int) else None)
        if left_type and right_type and left_type != right_type:
            print(f"Erro semântico: Operação inválida entre {left_type} e {right_type}.")

def p_action(p): 
    '''action : assignment SEMICOLON
              | LBRACE body RBRACE'''
    pass

def p_assignment(p):
    '''assignment : IDENTIFIER EQUAL expression '''
    if p[1] not in symbol_table:
        print(f"Erro semântico: Variável '{p[1]}' não foi declarada antes da atribuição.")

def p_error(p):
    if p:
        print(f"Erro de sintaxe! Token inesperado: {p.value}, linha {p.lineno}")
    else:
        print("Erro de sintaxe! Fim inesperado do código.")

parser = yacc.yacc()

codigo_exemplo = """
TYPE_INT x ROW RETURN TYPE_INT y FUNC soma {
    IF (x > 10) THEN {
        y = y + 1;
    }
    WHILE (x < 100) DO {
        x = x * 2;
    }
    FROM i = 1 TO 10 DO {
        x = x + i;
    }
}
"""

print("\nAnalisando a gramática:")
parser.parse(codigo_exemplo)
print("Código analisado com sucesso!")

#COISAS PARA MELHORAR
#TIRAR O ROW