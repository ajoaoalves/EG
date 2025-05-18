# GRAMMAR

SA( start ) { comp: int, soma:int, max:int }
SA( elems) { comp: int, soma:int, max:int }
SA( elem) { value:int }

start : "("  elems  ")"
ER { 
    start.comp = elems.comp;
    start.soma = elems.soma;
    start.max = elems.max;
}
TR { 
   print(start.comp, start.soma, start.max); 
}
elems : elem
ER {
    elems.comp = 1;
    elems.soma = elem.value;
    elems.max = elem.value; 
}
| elems "," elem
ER { 
elems[1].comp = elems[2].comp + 1;
elems[1].soma = elems[2].soma + elem.value;
elems[1].max = elems[2].max if(elems[2].max >= elem.value) else elem.value;
}
elem : NUM
ER {
   elem.value = int(NUM);
}
|  PAL
ER {
   elem.value = 0; 
}

NUM : /-?\d+/
PAL  : /[a-zA-Z_]\w*/

# INPUT

(1,2,a)

# GENERATED GRAMMAR

start : "(" elems ")" -> start_0
elems : elem -> elems_0 | elems "," elem -> elems_1
elem : NUM -> elem_0 | PAL -> elem_1
NUM : /-?\d+/
PAL : /[a-zA-Z_]\w*/

%import common.WS
%ignore WS

# GENERATED CODE

from lark import Lark, Token, Tree
from lark.visitors import Interpreter

class MyInterpreter(Interpreter):
    def __helper__(self, node):
        pointers={}
        pointers[node.data.split('_')[0]] = [node]
        for child in node.children:
            name = ''
            if type(child) == Tree:
                name = child.data.split('_')[0]
            elif type(child) == Token:
                name = child.type
            if name not in pointers:
                pointers[name] = []
            pointers[name].append(child)
        return pointers

    def start_0(self, node):
        pointers = self.__helper__(node)
        self.visit(pointers['elems'][0])
        node.comp = pointers['elems'][0].comp
        node.soma = pointers['elems'][0].soma
        node.max = pointers['elems'][0].max
        print(node.comp, node.soma, node.max)

    def elems_0(self, node):
        pointers = self.__helper__(node)
        node.comp = 1
        self.visit(pointers['elem'][0])
        node.soma = pointers['elem'][0].value
        node.max = pointers['elem'][0].value

    def elems_1(self, node):
        pointers = self.__helper__(node)
        self.visit(pointers['elems'][1])
        node.comp = pointers['elems'][1].comp + 1
        self.visit(pointers['elem'][0])
        node.soma = pointers['elems'][1].soma + pointers['elem'][0].value
        node.max = pointers['elems'][1].max if(pointers['elems'][1].max >= pointers['elem'][0].value) else pointers['elem'][0].value

    def elem_0(self, node):
        pointers = self.__helper__(node)
        node.value = int(pointers['NUM'][0])

    def elem_1(self, node):
        pointers = self.__helper__(node)
        node.value = 0
    
# Output

3 3 2