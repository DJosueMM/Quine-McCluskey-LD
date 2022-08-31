#Librerias
"""
PyEDA https://github.com/cjdrake/pyeda incluye una extensión de la librería de Espresso original-
  La librería es oficial, sin embargo, fue necesario añadir un binario en formato wheel(.whl) https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyeda
  no oficial de python el cuál solo funciona para Python 3.9 (o inferiores con un nuevo archivo .whl)
"""
from pyeda.inter import * 
import string


#VARIABLES GLOBALES
Y6var = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0" 


#FUNCIONES


def ObtenerYtts (minterminos, Y):
    
    Y6var_lista = Y.split(",")
    
    minTer = minterminos  
    minTer_int = list(map(int,  minTer))
    Y6var_int_list = list(map(int, Y6var_lista))
    

    for i in minTer_int :
        Y6var_int_list[i] = 1
    
   
    Y6var_int_list = list(map(str, Y6var_int_list))
    Ytts = "".join(Y6var_int_list)
   
    return Ytts



def EspressoMin (num_variables,Ytts):
    X = ttvars('x', num_variables)
    fbool = truthtable(X,Ytts)
    fboolm = espresso_tts(fbool)
    return fboolm

#----------------------------------------------------------------------------------------------------------------------------------


""" SOLICITUD DE DATOS AL USUARIO -----------------------------------------------------------------------------------------------"""

string_Minterms = input("Suma de minterminos:  ")
minterminos_Lista = string_Minterms.split(",")  # Con esto cada mintermino se mete en una lista

num_variables = int(input("Cantidad de variables: "))

print("\n") 


print(EspressoMin(num_variables, ObtenerYtts(minterminos_Lista, Y6var)))

