
GA = < GIC (<T, N, S, P={p: X->(N U T)*} ) , A, ER, CC, TR >

 A = U A(X), X€N    A(X) = SA(X) U IA(X)
AInt(t), t€T

1. listaMista : "("  elems  ")"
ER	        { listaMista.comp = elems.comp;
              listaMista.soma = elems.soma  }
TR          { escrever (listaMista.comp, listaMista.soma) }
2. elems  :    elem
ER	      { elems.comp = 1;
            elems.soma = elem.val }
3.         |   elems  "," elem
ER	      { elems1.comp = elems2.comp + 1;
            elems1.soma = elems2.soma + elem.val }
4. elem : NUM
ER	    { elem.val = NUM.val }
5.        |  PAL
ER	    { elem.val = 0 }

NUM : /-?\d+/
PAL  : /[a-zA-Z_]\w*/
