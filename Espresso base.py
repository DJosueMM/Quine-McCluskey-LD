#Librerias
"""
PyEDA https://github.com/cjdrake/pyeda incluye una extensión de la librería de Espresso original-
  La librería es oficial, sin embargo, fue necesario añadir un binario en formato wheel(.whl) https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyeda
  no oficial de python el cuál solo funciona para Python 3.9 (o inferiores con un nuevo archivo .whl)
"""
from pyeda.inter import * 
import string


#FUNCIONES


"Se construye la dimensión de la columna Y de la tabla de verdad en función de la cantidad de variables escogidas"
def ConstruirY (num_variables): 
    
    Yvar = "0"  
    Yaux = ",0" 
    
    for i in range(1,(2**num_variables),1):
        Yvar = Yvar+Yaux
        
    return Yvar #Se retorna el string base de 2**n ceros


"Se construye la columna Y de la tabla de verdad en función de la suma de minterminos"
def ObtenerYtts (minterminos, Y): #Se recibe una lista de mintérminos y una "máscara" de la columna Y con 2**n ceros
    
    Y6var_lista = Y.split(",") 
    
    minTer = minterminos  
    minTer_int = list(map(int,  minTer))
    Y6var_int_list = list(map(int, Y6var_lista))
    
    for i in minTer_int :
        Y6var_int_list[i] = 1
    
    Y6var_int_list = list(map(str, Y6var_int_list))
    Ytts = "".join(Y6var_int_list)
   
    return Ytts #Se retorna la columna Y de la tabla de verdad 


"Minimización de tablas de verdad con el algoritmo Espresso"
def EspressoMin (num_variables,Ytts): #Se recibe la cantidad de variables y las salidas de la tabla de verdad
    
    X = ttvars('x', num_variables) #Se diferencian las variables de acuerdo a su posición
    fbool = truthtable(X,Ytts) #Se define la función booleana con las variables y la tabla de verdad
    fboolm = espresso_tts(fbool) #Se minimiza la función booleana
    
    return fboolm #Se retorna la función booleana minimizada

#----------------------------------------------------------------------------------------------------------------------------------

""" SOLICITUD DE DATOS AL USUARIO -----------------------------------------------------------------------------------------------"""

string_Minterms = input("Suma de minterminos:  ")
minterminos_Lista = string_Minterms.split(",")  # Con esto cada mintermino se mete en una lista

num_variables = int(input("Cantidad de variables: "))

print("\n") 

Y = ConstruirY(num_variables) #Se construye las salidas de la tabla de verdad
print(EspressoMin(num_variables, ObtenerYtts(minterminos_Lista,Y))) #Se implementa la minimización con Espresso

