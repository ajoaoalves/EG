from lark import Lark,Transformer,Discard
from lark.tree import pydot__tree_to_png


grammar1 = '''
?start: value
?value: object
| array
| string
| SIGNED_NUMBER -> number
| "true" -> true
| "false" -> false
| "null" -> null
array : "[" [value ("," value)*] "]"
object : "{" [pair ("," pair)*] "}"
pair : string ":" value
string : ESCAPED_STRING
%import common.ESCAPED_STRING
%import common.SIGNED_NUMBER
%import common.WS
%ignore WS

'''

frase = '''
{"locations":[{
"name":"stand1",
"adress":"street 1",
"id":1},
{"name":"stand2",
"adress":"street 2",
"id":2}],
"inventory":[{
"model":"Tesla Model 3",
"year": 2024,
"kms":15000,
"type":"eletric",
"locationID": 1,
"plate": "AO-81-DN"}]}
'''

p = Lark(grammar1)
tree = p.parse(frase)

class Transformercarros(Transformer):
    def __init__(self):
        self.palavrasreservadaslocations = {"name", "adress", "id"}
        self.palavrasreservadasinventory = {"model","year", "kms", "type", "locationID", "plate"}
        self.stands = set()
        self.erro = []

    def start(self, tree):
        #print("start", tree)
        return Discard

    def number(self, tree):
        #print("number", tree)
        return int(tree[0])
    
    def true(self, tree):
        #print("true", tree)
        return True
    
    def false(self, tree):
        #print("false", tree)
        return False
    
    def null(self, tree):
        #print("null", tree)
        return None
    
    def array(self, tree):
        #print("array", tree)
        return tree
    
    def object(self, tree):
        print("object", tree)

        for t in tree:
            if t[0] == "locations":
                for elemento in t[1][0]: #porque tenho [[a]] e quero [a]
                    if elemento[0] not in self.palavrasreservadaslocations:
                        self.erro.append(f"Erro: {elemento[0]} não é uma palavra reservada em locations")
                    if elemento[0] == "id" and elemento[1] not in self.stands:
                        self.stands.add(elemento[1])
            if t[0] == "inventory":
                for elemento in t[1][0]:
                    if elemento[0] not in self.palavrasreservadasinventory:
                        self.erro.append(f"Erro: {elemento[0]} não é uma palavra reservada em inventory")
                    if elemento[0] == "year":
                       if elemento[1] < 2024:
                           self.erro.append(f"Erro: {elemento[0]} não pode ser inferior a 2024")
                    if elemento[0] == "locationID":
                        if elemento[1] not in self.stands:
                            self.erro.append(f"Erro: Localização de stand não existe")

        return tree
    
    def pair(self, tree):
        key = tree[0].strip('"')
        val = tree[1]
        return (key, val)

    
    def string(self, tree):
        return str(tree[0])
    
data = Transformercarros()
data.transform(tree)

for a in data.erro:
    print(a)    
