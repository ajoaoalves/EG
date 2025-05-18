SA(start) { comp: int, soma:int, max:int }
SA(elems) { comp: int, soma:int, max:int, cxt:str   }
SA(elem)  { val:int, maxant:int, max:int, ok:bool, sinalo:str }
IA(elem)  { sinali:str }

start :
"("  elems  ")"
ER	{ start.comp = elems.comp;
          start.soma = elems.soma;
          start.max  = elems.max;}
TR	{ print( start.comp );
          print( start.soma );
          print( start.max  ); }

elems  :
elem
ER	{ elems.comp = 1;
          elems.soma = elem.val;
          elems.max  = elem.val;
          elem.sinali = '?';
          elems.cxt = elem.sinalo; }
TR  { print(elem.ok); }

|  elems  "," elem
ER	{ elems[1].comp = elems[2].comp + 1;
          elems[1].soma = elems[2].soma + elem.val;
          elems[1].max  = elems[2].max if (elems[2].max>=elem.val) else elem.val;
          elem.sinali = elems[2].cxt;
          elems[1].cxt = elem.sinalo;  }
TR {  print(elem.ok); }

elem :
NUM
ER	{ elem.val = int(NUM);
          elem.ok = (elem.sinali == "p" and int(NUM)>=0) or (elem.sinali == "n" and int(NUM)<0) ;
          elem.sinalo = elem.sinali;  }
|  PAL
ER	{ elem.val = 0;
          elem.ok = True;
          elem.sinalo  = str(PAL); }

NUM : /-?\d+/
PAL  : /[a-zA-Z_]\w*/