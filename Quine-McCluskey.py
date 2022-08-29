
""" SOLICITUD DE DATOS AL USUARIO -----------------------------------------------------------------------------------------------"""

string_Minterms = input("Suma de minterminos:  ")
minterminos_Lista = string_Minterms.split(",")  # Con esto cada mintermino se mete en una lista

num_variables = int(input("Cantidad de variables: "))

print("\n")

""" TRATAMIENTO DE LOS MINTERMINOS: CONVERSION A BINARIO ---------------------------------------------------------------------------
Se usará la función bin() para convertir a binario cada mintermino (suponiendo que la tabla de verdad estaba ordenada y cada minterm
corresponde a su num en binario). Luego se debe lidiar con unos prefijos que devuelve esa funcion (esto por medio de una nueva
funcion llamada convertir_a_binario). Posteriormente, cada valor binario se ingresa en una nueva lista llamada lista_Bin_Minterms """

lista_Bin_Minterms = []         # Creamos una lista

def agregar_ceros(num):         # Esta funcion recibe un string
    largo = len(num)
    if largo < num_variables:
        diferencia = abs(largo - num_variables)
        new_num = num.rjust(diferencia + largo, "0")
        #print("New num: " + str(new_num))
        return new_num
    else:
        return num

def convertir_a_binario(num, flag):   # Esta funcion recibe un string
    bin_Num = bin(int(num))     # Python nos facilita el convertir a binario un int, pero nos retorna un string con el prefijo "0b"
    bin_Num_new = bin_Num.replace("0b", "")     # Eliminamos el prefijo "0b" para que no estorbe
    
    if flag == True:
        bin_Num_final = agregar_ceros(bin_Num_new)
        return bin_Num_final          # Esta funcion retorna un string
    else:
        return bin_Num_new

for minterm in minterminos_Lista:
    bin_Minterm = convertir_a_binario(minterm, True)
    print(bin_Minterm)
    lista_Bin_Minterms.append(bin_Minterm)

print("\n")


""" MANEJO DE POSIBLES ERRORES ----------------------------------------------------------------------------------------------------
Se parte del hecho de que si tenemos N variables, habra (2^N - 1) minterminos existentes en la tabla de verdad. Sin embargo,
para evitar errores posteriores se enviara un mensaje en caso de que el usuario no recuerde este detalle """

minterminos_Lista.sort() # Ordenamos la lista asi: [menor, ..., mayor]
length = len(minterminos_Lista)
elem_mayor = length - 1 # Ubicamos el elemento mayor (sera el ultimo) en la lista
excede = int(minterminos_Lista[elem_mayor]) > int(convertir_a_binario(num_variables, False)) # Variable booleana para verificar si hay error o no

if excede == True:
    print("Los datos ingresados no tienen sentido. Uno de los minterminos en binario es mayor que el numero de variables que usted especificó")
    exit

"""AGRUPAMIENTO DE MINTERMINOS SEGUN CANTIDAD DE 1's ---------------------------------------------------------------------------
Se clasifica a los minterms binarios segun su cantidad de unos y dicha informacion se guarda en un diccionario  (dict_grupos)
que contiene una lista para cada agrupacion. Como se solicito que funcionara para 4,5 y 6 variables, necesitamos unicamente 7
agrupaciones en el diccionario. Sin embargo se agregó una adicional."""

dict_grupos = {"0": [], "1": [], "2": [], "3": [], "4": [], "5": [], "6": []}   # Creamos un diccionario

def contar_unos(minterm): # Esta funcion recibe un string
    cantidad_unos = 0
    for digito in minterm:
        if digito == "1":
            cantidad_unos += 1
    #print(cantidad_unos)
    return str(cantidad_unos) # Esta funcion retorna un int convertido en string
            


for bin_Minterm in lista_Bin_Minterms:
    dict_grupos[contar_unos(bin_Minterm)].append(bin_Minterm)
    
print("\n")    
print(dict_grupos.items())    




