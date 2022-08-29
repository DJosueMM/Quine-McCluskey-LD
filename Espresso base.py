#Librerias
"""
PyEDA https://github.com/cjdrake/pyeda incluye una extensión de la librería de Espresso original-
  La librería es oficial, sin embargo, fue necesario añadir un binario en formato wheel(.whl) https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyeda
  no oficial de python el cuál solo funciona para Python 3.9 (o inferiores con un nuevo archivo .whl)
"""
from pyeda.inter import * 

import string

#----------------------------------------------------------------------------------------------------------------------------------

#Implementación básica en consola:
    
a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z = map(exprvar, string.ascii_lowercase) #Literales

lf1 = Or((a&b&c),(~a&~b&c),(~a&~b&c),(~a&~b&~c)) 

f1m = espresso_exprs(lf1)

print(f1m)
