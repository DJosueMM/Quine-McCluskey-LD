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

lf1 = Or((a&b&c),(~a&~b&c),(~a&~b&c),(~a&~b&~c)) #Función Booleana inicial

f1m = espresso_exprs(lf1) #Minimización mediante Espresso

print(f1m)


""" SOLICITUD DE DATOS AL USUARIO -----------------------------------------------------------------------------------------------"""

string_Minterms = input("Suma de minterminos:  ")
minterminos_Lista = string_Minterms.split(",")  # Con esto cada mintermino se mete en una lista

num_variables = int(input("Cantidad de variables: "))

print("\n") 


def ObtenerY ():
    
    Y6var = "---------------------------------------------------------------" 
    
    
    
    
    return Yval

def EspressoMin (num_variables,Yval):
    X = ttvars('x', num_variables)
    fbool = truthtable(X, "0000011111------------------------------------------------------")
    fboolm = espresso_tts(fbool)
    return fboolm

print(EspressoMin(num_variables,1))

