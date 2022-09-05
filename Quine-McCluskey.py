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
    print(" \n Entradas invalidas")
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

print(" \nAgrupacion inicial: ", conjuntos.items()) #Imprimir mints binarios

""" ENCONTRAR IMPLICANTES PRIMOS ---------------------------------------------------------------------------------------
Se necesita comparar un mintermino perteneciente a una agrupacion con otro de una agrupacion superior de unos.
Para esto, se evalua cada digito de ambos minterminos: primero se verifica que solo una posicion cambie entre ellos. 
Posteriormente, se evalua cual posicion fue la que cambio, y se procede a poner un guión '-' en su lugar. Esta nueva 
informacion se guarda en el mismo diccionario utilizado para agrupar segun cantidad de unos, pero se elimina su 
contenido en cada iteración para así no tener que crear diccionarios a cada rato. Este algoritmo iterativo se detiene 
cuando ya los minterminos tienen más de una diferencia. """
backup = {}
no_puedo_seguir_comparando = True
agrup = 0
mints_implic_primos = []
todos_los_dict = []

while True: # ALGORITMO PARA COMPARAR ITERATIVAMENTE
    #print("Estoy en el while")
    #print()

    # quiero comparar hasta que ya no se pueda = los bin_mints ya no se pueden comparar con los de los demas grupos
    # comparar =  ver si solo difieren en 1 digito (bit)
    backup = conjuntos.copy()
    conjuntos = {} #Diccionario se limpia para comparar cada vez
    no_puedo_seguir_comparando = True
    # para todos los bin_mints de todos los conjuntos: pero cuantos conjuntos hay actualmente?
    grupos_existentes = sorted(list(backup.keys()))
    largo_grupos_existentes = len(grupos_existentes) - 1

    # para saber cual agrupacion usar
    agrup = 0

    for grupo_actual in range(largo_grupos_existentes): # hacerlo para todos los grupos
        for mint_del_grupo1 in backup[grupos_existentes[grupo_actual]]: # elijo el grupo1
            for mint_del_grupo2 in backup[grupos_existentes[grupo_actual + 1]]: # elijo el grupo2

                # evaluar diferencias
                difiere = 0
                for digito in range(len(mint_del_grupo1)):
                    if mint_del_grupo1[digito] != mint_del_grupo2[digito]:
                        difiere += 1
                        index_diferencia = digito

                if difiere == 1:
                    try:
                        conjuntos[agrup].append(str(mint_del_grupo1[:index_diferencia] + "-" + mint_del_grupo1[index_diferencia + 1:]))
                    except KeyError:
                        conjuntos[agrup] = [str(mint_del_grupo1[:index_diferencia] + "-" + mint_del_grupo1[index_diferencia + 1:])]

                    no_puedo_seguir_comparando = False

        agrup += 1

    #print("Conjuntos ", conjuntos)
    todos_los_dict.append(conjuntos)

    if no_puedo_seguir_comparando:
        break


"""OBTENER IMPLICANTES PRIMOS ESENCIALES--------------------------------------------------------------------------------
Para saber cuales minterminos componen a los implicantes primos, se creo una funcion que devuelve una lista compuesta
por estos minterminos en su representacion de int. Con estos datos, se cuentan las apariciones de cada mintermino, 
para asi determinar que los implicantes primos esenciales son aquellos que solo aparecen una vez. """

mints_sin_repeticion = set()

def obtener_minterms_padres(mint_con_guiones): # Recibe un mintermino con guiones y devuelve los minterminos que lo componen
    num_de_guiones = mint_con_guiones.count('-')

    if num_de_guiones == 0:
        return [str(int(mint_con_guiones, 2))]

    permutaciones = [bin(num)[2:].zfill(num_de_guiones) for num in range(2**num_de_guiones)]
    mints_padres = []

    for num in range(2**num_de_guiones):
        mintPadre = mint_con_guiones[:]
        index = -1

        for digito in permutaciones[0]:
            #print("Permutacion ", permutaciones[0])
            if index != -1:
                index = index + mintPadre[index + 1:].find('-') + 1
            else:
                index = mintPadre[index + 1:].find('-')

            mintPadre = mintPadre[:index] + digito + mintPadre[index + 1:]

        int_mintPadre = str(int(mintPadre, 2))
        mints_padres.append(int_mintPadre)
        mints_sin_repeticion.add(int_mintPadre)

        permutaciones.pop(0)

    return mints_padres

# RECONSTRUIR MINTERMINOS
ultimo_dict = todos_los_dict[len(todos_los_dict)-2] #El ultimo diccionario util es el penultimo
imp_prim = list(ultimo_dict.values()) #Lista de listas con los minterminos con guiones

#Esta parte es para lidiar con algunos errores-------------------------------
set_1D = set()
for sub_lista in range(len(imp_prim)):
    for elem in imp_prim[sub_lista]:
        set_1D.add(elem)

implicantes_primos = []
for elem in set_1D:
    implicantes_primos.append(elem)
#----------------------------------------------------------------------------

print("Implicantes primos en binario ", implicantes_primos)

for imp in range(len(implicantes_primos)): # para cada implicante primo en bin
    mints_implic_primos += [obtener_minterms_padres(implicantes_primos[imp])] #Obtencion de los ints

print("Implicantes primos en int ", mints_implic_primos)

#Hacer que la lista solo sea de una dimension
list_mints_imp_primos = []

for sub_lista in mints_implic_primos:
    list_mints_imp_primos += sub_lista

#Contar apariciones de cada mintermino
dict_apariciones = {}

for mint in mints_sin_repeticion:
    dict_apariciones[mint] = list_mints_imp_primos.count(mint)
print("Apariciones de cada imp. primo: ", dict_apariciones.items())

imp_esenciales = []

for int_mint,apariciones in dict_apariciones.items():
    if apariciones == 1:
        imp_esenciales.append(int_mint)

print(" \n Implicantes primos esenciales: ", imp_esenciales)

""" RESPUESTA FINAL CON LETRAS USANDO LOS IMPLICANTES PRIMOS ESENCIALES-------------------------------------------------
"""
#Usar los minterminos donde aparecen los impl. p. esenciales
