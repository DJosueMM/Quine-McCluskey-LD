
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
dict_bin_and_nums = {}          # Diccionario de tipo {"2" : "0010", "3" : "0011"}

def agregar_ceros(num):         # Esta funcion recibe un string
    largo = len(num)
    if largo < num_variables:
        diferencia = abs(largo - num_variables)
        new_num = num.rjust(diferencia + largo, "0")
        #print("New num: " + str(new_num))
        return new_num
    else:
        return num

def convertir_a_binario(num, flag):             # Esta funcion recibe un string
    bin_Num = bin(int(num))                     # Python nos facilita el convertir a binario un int, pero nos retorna un string con el prefijo "0b"
    bin_Num_new = bin_Num.replace("0b", "")     # Eliminamos el prefijo "0b" para que no estorbe
    
    if flag == True:
        bin_Num_final = agregar_ceros(bin_Num_new)
        dict_bin_and_nums.update({bin_Num_final : int(num)})    # Diccionario para guardar cual binario corresponde a cada int
        return bin_Num_final                    # Esta funcion retorna un string

    else:
        return bin_Num_new

for minterm in minterminos_Lista:
    bin_Minterm = convertir_a_binario(minterm, True)
    #print(bin_Minterm)
    lista_Bin_Minterms.append(bin_Minterm)

print("\n")
#print("Correspondencia ")
#print(dict_bin_and_nums.items())

""" MANEJO DE POSIBLES ERRORES ----------------------------------------------------------------------------------------------------
Se parte del hecho de que si tenemos N variables, habra (2^N - 1) minterminos existentes en la tabla de verdad. Sin embargo,
para evitar errores posteriores se enviara un mensaje en caso de que el usuario no recuerde este detalle """

minterminos_Lista.sort()    # Ordenamos la lista asi: [menor, ..., mayor]
length = len(minterminos_Lista)
elem_mayor = length - 1     # Ubicamos el elemento mayor (sera el ultimo) en la lista
excede = int(minterminos_Lista[elem_mayor]) > int(convertir_a_binario(num_variables, False))    # Variable booleana para verificar si hay error o no

if excede == True:
    print("Los datos ingresados no tienen sentido. Uno de los minterminos en binario es mayor que el numero de variables que usted especificó")
    exit

"""AGRUPAMIENTO DE MINTERMINOS SEGUN CANTIDAD DE 1's ---------------------------------------------------------------------------
Se clasifica a los minterms binarios segun su cantidad de unos y dicha informacion se guarda en un diccionario  (dict_grupos)
que contiene una lista para cada agrupacion. Como se solicito que funcionara para 4,5 y 6 variables, necesitamos unicamente 7
agrupaciones en el diccionario. Sin embargo se agregó una adicional."""

dict_grupos = {"0": [], "1": [], "2": [], "3": [], "4": [], "5": [], "6": []}   # Creamos un diccionario

def contar_unos(minterm):       # Esta funcion recibe un string
    cantidad_unos = 0
    for digito in minterm:
        if digito == "1":
            cantidad_unos += 1
    #print(cantidad_unos)
    return str(cantidad_unos)   # Esta funcion retorna un int convertido en string
            

for bin_Minterm in lista_Bin_Minterms:
    dict_grupos[contar_unos(bin_Minterm)].append(bin_Minterm)
    
print("\n BINARIOS AGRUPADOS SEGUN CANTIDAD DE UNOS: \n")    
print(dict_grupos.items())
print("\n \n ")


""" COMBINACION DE GRUPOS SEGUN CANTIDAD DE 1's ----------------------------------------------------------------------------
Se necesita comparar un mintermino perteneciente a una agrupacion con otro de una agrupacion superior de unos.
Para esto, se evalua cada digito de ambos minterminos: primero se verifica que solo una posicion cambie entre ellos. Posteriormente,
se evalua cual posicion fue la que cambio, y se procede a poner una X en su lugar. Esta nueva informacion se guarda en un nuevo
diccionario {[mint INT, mint INT] : [mint STRING, Numero de 1's] } """

lista_minterms_incluidos = [] # lista para incluir a los minterms (num en int) que ya se incluyeron a otra lista pero con la x
lista_minterms_con_x = [] # minterminos revisados pero con una x en donde hay 1 diferencia. Luego esta lista se revisara con comparar_grupos2 para verificar si hay mas de una diferencia


def comparar_grupos(first, second, primera_etapa_flag):
    diferencias = 0
    posiciones_distintas = []
    diferentes = False
    tiene_x = False

    primera_agrup = ""
    segunda_agrup = ""

    print(str(len(dict_grupos[first])) + str(len(dict_grupos[second])))

    if primera_etapa_flag:
        primera_agrup = dict_grupos[first]
        segunda_agrup = dict_grupos[second]
    else:
        primera = "" # pendiente
        segunda = "" # pendiente
    
    if primera_agrup != [] and segunda_agrup != []:
        for i in range(0, len(primera_agrup)): # para cada mintermino en la agrupacion 1
            print("I" + str(i))
            for j in range(0, len(segunda_agrup)): # para cada mintermino en la agrupacion 2
                print("J" + str(j))
                for k in range(0, num_variables): # para cada digito en ambos minterminos
                    print("K" + str(k))
                        
                    print("Comparando " + primera_agrup[j] + " " + segunda_agrup[j])

                    diferentes = primera_agrup[i][k] != segunda_agrup[j][k]
                    no_tienen_x = primera_agrup[i][k] != "x" and segunda_agrup[j][k] != "x"
                
                    if diferentes and no_tienen_x: # si no son iguales, aumentar el num de diferencias. Si sí tienen X
                        diferencias += 1
                        if diferencias > 1: # si sobrepasa el limite de diferencias, descartar el num
                            break

                        else: # si no lo sobrepasa, marcarlo con una X y guardarlo en una estructura de datos (pendiente lo de guardarlo)
                            #dict_grupos[second][i].replace(dict_grupos[second][i][k], "x")
                            print(str(primera_agrup[i][:k] + "x" + segunda_agrup[i][k+1:]))
                            
                            
    else:
        print("Agrupacion vacia")
    

                        
                    
def iterar_comparar_grupos(): # esta funcion es para que la funcion de comparar se realice varias veces, cada vez con un par de agrupaciones sucesivas
    comparar_grupos("0", "1", True)
    comparar_grupos("1", "2", True)
    comparar_grupos("2", "3", True)
    comparar_grupos("3", "4", True)
    comparar_grupos("4", "5", True)
    comparar_grupos("5", "6", True)

    # abajo se supone que siguen las comparaciones usando la otra estructura de datos

    

iterar_comparar_grupos()
