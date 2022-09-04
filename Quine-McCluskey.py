""" Algoritmo Quine-McCluskey: simplificacion de expresiones booleanas
Estudiantes: Jimena León Huertas y David Josué Medina Mayorga | ITCR Diseño Logico"""

""" SOLICITUD DE DATOS AL USUARIO --------------------------------------------------------------------------------------
"""
int_mints = [int(mint) for mint in input("Suma de mintérminos ").split(",")]  #Genera lista con ints
vars = int(input("Cantidad de variables: "))


"""TRATAMIENTO DE ERRORES-----------------------------------------------------------------------------------------------
Se parte del hecho de que si tenemos N variables, habra (2^N - 1) minterminos existentes en la tabla de verdad. Sin 
embargo, para evitar errores posteriores se enviara un mensaje en caso de que el usuario no recuerde este detalle. """
int_mints.sort()
if int_mints[len(int_mints)-1] > 2**vars - 1:  #Si tengo 2 variables, el mintérmino mayor debe ser el 3ro = 11 bin
    print("Entradas invalidas")
    exit()

""" CONVERSION A BINARIO DE LOS MINTERMINOS ----------------------------------------------------------------------------
Se usará la función bin() para convertir a binario cada mintermino (suponiendo que la tabla de verdad estaba ordenada 
y cada minterm corresponde a su num en binario). Se ignora un prefijo que devuelve la función utilizada y luego se 
rellena con ceros el num binario según la cantidad de variables especificada """
int_bin_mints = {}
for mint in int_mints:  #Añade binarios rellenados con N ceros (N = num de variables) en un diccionario
    int_bin_mints[mint] = bin(mint)[2:].zfill(vars) #{"2":  "00010"} ejemplo

"""AGRUPAMIENTO DE MINTERMINOS SEGUN CANTIDAD DE 1's -------------------------------------------------------------------
Se clasifica a los minterms binarios segun su cantidad de unos y dicha informacion se guarda en un diccionario  
(dict_grupos) que contiene una lista para cada agrupacion. No sabemos cuales agrupaciones hay, por lo tanto estas se 
crean segun la informacion que se vaya obteniendo. De esta forma, el algoritmo va a servir para n variables y nos 
ahorramos el tener que verificar si una agrupacion esta vacia o no. """
conjuntos = {}
for bin_mint in int_bin_mints.values():  #Contar 1's y añadir binarios en un nuevo diccionario
    try:
        conjuntos[bin_mint.count("1")].append(bin_mint)  #Añade al grupo existente
    except:
        conjuntos[bin_mint.count("1")] = [bin_mint]  #Crea nuevo grupo si antes no existía

#print(conjuntos.values()) #Imprimir mints binarios

""" ENCONTRAR IMPLICANTES PRIMOS ---------------------------------------------------------------------------------------
Se necesita comparar un mintermino perteneciente a una agrupacion con otro de una agrupacion superior de unos.
Para esto, se evalua cada digito de ambos minterminos: primero se verifica que solo una posicion cambie entre ellos. 
Posteriormente, se evalua cual posicion fue la que cambio, y se procede a poner un guión '-' en su lugar. Esta nueva 
informacion se guarda en el mismo diccionario utilizado para agrupar segun cantidad de unos, pero se elimina su 
contenido en cada iteración para así no tener que crear diccionarios a cada rato. Este algoritmo iterativo se detiene 
cuando ya los minterminos tienen más de una diferencia. """
