""" Programa KingCoffee: simplificacion de expresiones booleanas
Estudiantes: Jimena León Huertas y David Josué Medina Mayorga | ITCR Diseño Logico"""

from tkinter import *
from tkinter import filedialog as fld
from pyeda.inter import * 
import string
import time

#Se crea la clase madre "Quine" que implementa QN
class Quine(Frame):
    
    #Creando la ventana para la clase Quine
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("355x350+375+205")
        self.master.resizable(width=0, height=0)
        self.master.config(bg='Blue')
        self.create_widgets()

    #Creando los widgets que se verán en la ventana de QN
    def create_widgets(self):
        
        #Texto descriptivo
        self.texto=Text(self.master)
        self.texto.insert(INSERT, "El algoritmo de Quine-Mcluskey le dará una              minimización exacta de la funcion booleana. "
                          "Ingrese la suma de minterminos de la forma 0,1,2,...,61,62,63 y elija la cantidad de variables entre 1 y 6")
        self.texto.config(height=4,width=55,bg="#CDD1FE",font=("Arial",10))
        self.texto.pack(padx=17,pady=10)
        
        #Label para la sumatoria de minterminos
        self.eti=Label(self.master,text="Minterminos:")
        self.eti.config(bg="#CDD1FE", fg='black',font=('Arial',10))
        self.eti.place(x=40, y=95)
        
        #Entry para la sumatoria de minterminos
        self.E1 = Entry(self.master,bd = 7)
        self.E1.config(width=30)
        self.E1.pack(pady=7,anchor=CENTER)
        self.E1.place(x=130, y=90)
        
        #Label para el numero de variables
        self.eti=Label(self.master,text="Número de variables:")
        self.eti.config(bg="#CDD1FE", fg='black',font=('Arial',10))
        self.eti.place(x=55, y=135)
        
        #Entry para el numero de variables
        self.E2 = Entry(self.master,width=10)
        self.E2.place(x = 190,y = 135)

        #Botón Minimizar
        self.boton_Quine = Button(self.master, text="Minimizar",command=self.QN)
        self.boton_Quine.place(x=135,y=220)
        self.boton_Quine.config(bd=10, relief=RAISED)
        self.boton_Quine.config(bg='#154360',fg='white',font=('Arial',11,'bold normal'))
        
        #Botón Limpiar
        self.boton_Quine = Button(self.master, text="Limpiar",command=self.Limpiar_QN)
        self.boton_Quine.place(x=70,y=290)
        self.boton_Quine.config(bd=10, relief=RAISED)
        self.boton_Quine.config(bg='#154360',fg='white',font=('Arial',11,'bold normal'))
        
        #Botón Salir
        self.boton_salir = Button(self.master, text="Salir",command=self.salir)
        self.boton_salir.place(x=215,y=290)
        self.boton_salir.config(bd=10, relief=RAISED)
        self.boton_salir.config(bg='#154360',fg='white',font=('Arial',11,'bold normal'))
        
    """
    Minimización por Quine-Mcluskey
    """
    def QN(self):
        
        #Recupera los datos ingresados en la ventana
        int_mints = [int(mint) for mint in self.E1.get().split(",")]  #Genera lista con ints
        vars = int(self.E2.get())
        
    
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
    
                        if difiere == 1: # añadir el implicante primo al diccionario de conjuntos
                            try:
                                conjuntos[agrup].append(str(mint_del_grupo1[:index_diferencia] + "-" + mint_del_grupo1[index_diferencia + 1:]))
                            except KeyError:
                                conjuntos[agrup] = [str(mint_del_grupo1[:index_diferencia] + "-" + mint_del_grupo1[index_diferencia + 1:])]
    
                            no_puedo_seguir_comparando = False
    
                agrup += 1

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
    
    
        for imp in range(len(implicantes_primos)): # para cada implicante primo en bin
            mints_implic_primos += [obtener_minterms_padres(implicantes_primos[imp])] #Obtencion de los ints
    
    
        #Hacer que la lista solo sea de una dimension
        list_mints_imp_primos = []
    
        for sub_lista in mints_implic_primos:
            list_mints_imp_primos += sub_lista
    
        #Contar apariciones de cada mintermino
        dict_apariciones = {}
    
        for mint in mints_sin_repeticion:
            dict_apariciones[mint] = list_mints_imp_primos.count(mint)
    
        #Crear lista de implicantes primos esenciales en formato int
        imp_esenciales = []
    
        for int_mint,apariciones in dict_apariciones.items():
            if apariciones == 1:
                imp_esenciales.append(int_mint)

    
        """ RESPUESTA FINAL CON LETRAS USANDO LOS IMPLICANTES PRIMOS ESENCIALES-------------------------------------------------
        """
        #Usar los minterminos donde aparecen los impl. p. esenciales esta vez en formato binario con guiones
        respuesta = []
        for imp_esencial in imp_esenciales:
            for i in range(len(mints_implic_primos)):
                for j in mints_implic_primos[i]:
                    if imp_esencial == j:
                        respuesta.append(implicantes_primos[i])
        
        #Traducir al alfabeto los impl.primos esenciales
        variable = 0
        funcion = " "
        encabezado = "F("
        usadas = set()
        letras = ["A","B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "Ñ", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    
        for imp in range(len(respuesta)):
            for digito in respuesta[imp]:
                if digito == "0":
                    funcion = funcion + letras[variable] + "'"
                    usadas.add(letras[variable])
                if digito == "1":
                    funcion = funcion + letras[variable]
                    usadas.add(letras[variable])
    
                variable += 1
            variable = 0
    
            if imp != len(respuesta)-1:
                funcion = funcion + " + "
    
        largo = len(usadas)
        usadas_sorted = []
    
        for letra in usadas:
            usadas_sorted.append(letra)
    
        #Ordenamiento de letras para el encabezado
        usadas_sorted.sort()
    
        for letra in usadas_sorted:
            largo -= 1
            encabezado += letra
    
            if largo != 0:
                encabezado += ", "
            else:
                encabezado += ") = "
    
        stringFuncion = encabezado + funcion
        
        #Muestra el resultado de la función minimizada
        self.etiq=Label(self.master,text="La función minimizada es:\n"+stringFuncion)
        self.etiq.config(bg="#CDD1FE", fg='black',font=('Arial',9))
        self.etiq.pack(pady=40,anchor=CENTER)
        self.etiq.place(x=80, y=170)
        

        
    #Función Limpiar: Borra las entradas utilizadas por el usuario para poder minimizar nuevamente   
    def Limpiar_QN(self):
        self.E1.delete(0,END)
        self.E2.delete(0,END)
        self.etiq.destroy()
    
    #Función salir: destruye la ventana de QuineMcluskey y regresa a la ventana principal
    def salir(self):
        self.master.destroy()
        root.deiconify()
    

#Creando clase madre para Espresso
class Espresso(Frame):
    
    #Se crea la ventana de la clase Espresso
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("450x470+500+170")
        self.master.resizable(width=0, height=0)
        self.master.config(bg='Blue')
        self.create_widgets()
        self.menu()
        
    #Función para crear el menú superior
    def menu(self):
        self.menubar=Menu(self)
        self.menubar=Menu(self.master)
        self.opciones=Menu(self.menubar,tearoff=0)
        self.opciones.add_command(label="Minimizar", command = self.Minimizar_Espresso)
        self.opciones.add_command(label="Limpiar todo", command = self.Limpiar_espacios)
        
        self.opciones.add_separator()
        self.opciones.add_command(label="Salir",command=self.salir)
        
        self.menubar.add_cascade(label = "Opciones", menu = self.opciones)
        self.master.config(menu=self.menubar)
    
  

    #Se crean todos los widgets que irán en la ventana
    def create_widgets(self):
        
        #Label de Bienvenida
        self.etiq=Label(self.master,text="Espresso")
        self.etiq.config(bg='black', fg='yellow',font=('times',15,'bold italic'))
        self.etiq.place(x=90, y=20)
        
        #Texto descriptivo
        self.texto=Text(self.master)
        self.texto.insert(INSERT, "El algoritmo Espresso le dará una minimización de bajo costo de          ejecución. "
                          "Ingrese la suma de mintérminos de la forma (1,2,...,62,63)       y elija la cantidad de variables"         
                          " que quiera utilizar \n\nEn el menú de opciones puede obtener la función minimizada")
        self.texto.config(height=6,width=60,bg="#CDD1FE",font=("Arial",10))
        self.texto.pack(padx=10,pady=10)
        
       
        #Label numero de variables
        self.eti=Label(self.master,text="Numero de variables")
        self.eti.config(bg="#CDD1FE", fg='black',font=('Arial',10))
        self.eti.place(x= 80, y= 120)
      
        #Entry para el numero de variables
        self.valor_N = Entry(self.master,bd = 7, width=10)
        self.valor_N.place(x = 210, y = 115)
        
        #Label minterminos
        self.ingreso_info =Label(self.master,text="Minterminos:")
        self.ingreso_info.config(bg="#CDD1FE", fg='black',font=('Arial',11))
        self.ingreso_info.place(x= 80, y= 165)
         
        
        #Entry para la sumatoria de minterminos
        self.cod = Entry(self.master,bd = 7)
        self.cod.config(width=30)
        self.cod.pack(pady=7,anchor=CENTER)
        self.cod.place(x=210, y= 162, width= 200, height=35)
  
    
    #Función Limpiar_espacios: borra los datos ingresados por el usuario
    def Limpiar_espacios(self):
        
        self.cod.delete(0,END)
        self.texto.delete(1.0,END)
        self.valor_N.delete(0,END)

        
    def Minimizar_Espresso(self):
        
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
        

        #Recupera los datos ingresados por el usuario
        minterminos_Lista = [int(mint) for mint in self.cod.get().split(",")] 
        
        
        num_variables = int(self.valor_N.get())
  
        
        #Se construye las salidas de la tabla de verdad
        Y = ConstruirY(num_variables) 
        
        
        
        A = EspressoMin(num_variables, ObtenerYtts(minterminos_Lista,Y))

        
        #Textbox de la funcion minimizada
        self.texto=Text(self.master)
        self.texto.insert(INSERT, "La función minimizada es:\n"+str(A))
        self.texto.config(bg="#FFFFFF", fg='black',font=('Arial',9))
        self.texto.place(x=10, y=200, width= 400, height = 200)
        

        
    
    #Función salir: destruye la ventana de la clase Espresso y regresa a la ventana principal
    def salir(self):
        self.master.destroy()
        root.deiconify()
    

#Clase hija ventana principal, hereda las características de la clase Quine y Espresso
class Window(Frame):
    
    #Crea una ventana para la clase Window, que será la ventana principal del programa
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("270x270+500+175")
        self.master.resizable(width=0, height=0)
        self.master.config(bg='#2471A3')
        self.create_widgets()

    #Crea los widgets que se verán en la ventana principal
    def create_widgets(self):
        
        #Label de Bienvenida
        self.etiq=Label(self.master,text="Bienvenidos")
        self.etiq.config(bg='#154360', fg='white',height=1,width=10,borderwidth=3, relief="ridge",font=('times',15,'bold italic'))
        self.etiq.pack(anchor=CENTER, pady=10)
        
        #Texto descriptivo
        self.texto=Text(self.master)
        self.texto.insert(INSERT, "En este programa podrá minimizar          ecuaciones booleanas con los algoritmos de "
                          "Quine-McCluskey y Espresso, explore las diferentes funcionalidades de cada uno " )
        self.texto.config(height=5,width=35,bg="White",font=("Arial",10))
        self.texto.pack(padx=10,pady=15)
        
        #Botón para ir a QN
        self.boton_Quine = Button(self.master, text="Quine-Mcluskey",command=qn)
        self.boton_Quine.place(x=12,y=170)
        self.boton_Quine.config(bd=10, relief=RAISED)
        self.boton_Quine.config(bg='#154360',fg='white',font=('Arial',10,'bold normal'))
        
        #Botón para ir a Espresso
        self.boton_espp = Button(self.master, text="Espresso",command=espp)
        self.boton_espp.place(x=160,y=170)
        self.boton_espp.config(bd=10, relief=RAISED)
        self.boton_espp.config(bg='#154360',fg='white',font=('Arial',10,'bold normal'))
        
        
"""
Función que llama a la clase Quine, que implementa el algoritmo Quine-Mcluskey
"""
def qn():
    root.iconify() 
    vent_line = Tk()
    
    app = Quine(master=vent_line)
    app.master.title('Quine-Mcluskey')
    app.mainloop()

"""
Función que llama a la clase Espresso, que implementa el algoritmo Espresso
"""
def espp():
    root.iconify()
    vent_espp= Tk()
    ap=Espresso(master=vent_espp)
    ap.master.title("Espresso")
    ap.mainloop() 


#Programa que crea la ventana principal y llama a la clase Window
root = Tk()
app = Window(master=root)
app.master.title('KingCoffee')
app.mainloop() 