from lark import Lark, Transformer, UnexpectedToken

# Gramática JSON esperada
json_grammar = """
    ?start: object

    ?object: "{" [pair ("," pair)*] "}"

    ?pair: key ":" value

    ?key: ESCAPED_STRING

    ?value: ESCAPED_STRING 
          | NUMBER 
          | "{" [pair ("," pair)*] "}"
          | "[" [value ("," value)*] "]"

    %import common.ESCAPED_STRING
    %import common.NUMBER
    %import common.WS
    %ignore WS
"""

# Lista de chaves permitidas conforme o exemplo fornecido
RESERVED_KEYS = {
    "locations", "name", "adress", "id",
    "inventory", "model", "year", "kms",
    "type", "locationID", "plate"
}

# Definição do Transformer para validação
class JSONValidator(Transformer):
    def key(self, items):
        key_str = items[0][1:-1]  # Removemos as aspas do JSON
        if key_str not in RESERVED_KEYS:
            print(f"Erro: Chave inválida '{key_str}' encontrada.")
        return key_str

# Criar o parser
parser = Lark(json_grammar, parser='lalr', transformer=JSONValidator())

# JSON de entrada (como string)
json_input = '''
{
    "locations": [
        {
            "name": "stand1",
            "adress": "street 1",
            "id": 1
        },
        {
            "namyhyhyhyhye": "stand2",
            "adress": "street 2",
            "id": 2
        }
    ],
    "inventory": [{
        "model": "Tesla Model 3",
        "year": 2024,
        "kms": 15000,
        "type": "eletric",
        "locationID": 1,
        "plate": "AO-81-DN"
    }]
}
'''

# Executar validação
try:
    parser.parse(json_input)
except UnexpectedToken as e:
    print(f"Erro de sintaxe: {e}")
