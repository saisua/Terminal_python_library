import os
import sys

path_registro = str(os.getcwd()) + chr(92)
argumentos = sys.argv
verbose = 3

def printf(printed,verb):
    if verbose >= verb:
        print(printed)

def read_arg(argumentos, lista_argumentos):
    lista_variables = []
    variable_numero = 0
    for arg in argumentos:
        if arg[0] == "-":
            numero_variables = 0
            variable_numero = 0
            #analiza determina el argumento a dar, y que variables esperar
            argumento_analizado = analizar_argumento(arg, lista_argumentos)
            for tipos_variables in argumento_analizado:
                for numero_tipos in range(tipos_variables[1]):
                    lista_variables.append(tipos_variables[0])
        elif numero_variables != 0:
            variable_numero += 1
            if len(lista_variables) <= variable_numero:
                if lista_variables[variable_numero][0] == ":" or lista_variables[variable_numero][0] == ";":
                    lista_variables.append(lista_variables[variable_numero][0])
                    tipo = tipo_argumento(arg)


def analizar_argumento(arg, lista_argumentos):
    for listed_arg in lista_argumentos:
        if listed_arg == arg:
            print("Hola")
    return [["tipo de var, num"],"...."]

def tipo_argumento(arg):
    arg = str(type(arg))
    arg_type = arg[8:(len(arg)-2)]
    printf(arg_type,2)
    return arg_type

def abrir_archivo(path,modo):
    printf("Abriendo archivo " + str(path), 1)
    if modo == "r" or modo == "w" or modo == "a" or modo == "r+":
        printf("Modo aceptado " + str(modo), 2)
        if existe_fichero(path):
            archivo = open(path, modo)
            printf("archivo: " + str(archivo),3)
            if modo != "w" and modo != "a":
                archivo_abierto = archivo.read()
                printf("archivo abierto: " + str(archivo_abierto),2)
                return archivo_abierto
            return archivo
        else:
            printf("ERROR: el archivo " + str(path) + " no existe", 0)
            printf("",0)
            printf("Crear ahora? Y/n: ",0)
            inp = ""
            while inp == "":
                inp = str(input())
                if inp != "":
                    break
            if inp == "Y" or inp == "y":
                printf("Creando " + str(path),1)
                open(path, modo)
                printf("Archivo creado!",1)
                printf("Probar a abrir " + str(path) + "? Y/n:",0)
                inp = ""
                while inp != "":
                    inp = str(input())
                    if inp != "":
                        break
                if inp == "Y" or inp == "y":
                    abrir_archivo(path,modo)

    else:
        printf("ERROR: modo no permitido: " + str(modo),0)
        printf("Los modos permitidos son:", 0)
        printf("r = read        w = write",0)
        printf("a = append      r+ = read + write",0)


def leer_fichero(path, cantidad):
    #cantidad de tipo string separa
    #"1,2,-3 3-6,1 $hola$-"
    #el primer grupo, segundo subgrupo, desde el primer hasta el 3r elemento del subsubgrupo
    #del 3r grupo hasta el 6to, todos los 1r subgrupos
    #y desde el marcapaginas $hola$ hasta el final todo
    archivo = abrir_archivo(path,"r")
    group = 1
    final = []
    final_return = []
    valor = ""
    marcapaginas_valor = ""
    marcapaginas_lista = []
    contador = [0,0]
    guardar = False
    numero_guardar = []
    marcapaginas_guardar = []
    #marcapaginas_lista [[numero valor antes, numero valor despues],subgrupo]

    #marcapaginas guardar = [[marcapaginas, -1/1], ...]
    #numero guardar = [[pos,subgrupo,-1/0/1], ...] donde:
    #subgrupo = [1,2]
    #-1: guardar = false
    #0:  guardar no varía, pero almacenar el valor
    #1:  guardar = true
    guardar_num = 0
    guardar_pos = 0
    guardar_group = []
    anterior = 0
    subgroup = []
    cantidad += " "
    if tipo_argumento(cantidad) == "str":
        for kant in cantidad:
            guardar_pos = 0

            if kant == " ":
                if anterior == 1:
                    numero_guardar.append([contador[len(contador)],contador[0:len(contador)-1],guardar_num])
                elif anterior == -1:
                    marcapaginas_guardar.append(["$" + marcapaginas_valor + "$",guardar_num])
                elif anterior == 0 and guardar_num == -1:
                    numero_guardar.append([0,contador[0:len(contador)-1],1])
                anterior = 0
                guardar_num = 0
                contador = [0,0]
            elif kant == "-":
                if anterior == 0:
                    guardar_num = -1
                else:
                    guardar_num = 1
            elif kant == "$":
                anterior = -1
            elif kant == ",":
                guardar_num = 0
                anterior = 0
                group += 1
                while len(contador) < group:
                    contador.append(0)
            else:
                if anterior == -1:
                    marcapaginas_valor += kant
                else:
                    valor += kant
            contador[group] += 1
######################################

        marcapaginas_valor = ""
        valor = ""
        group = 0
        contador = [0,0]

####################################
        for letter in archivo:
            if letter == "[":
                group += 1
                while len(contador) < group + 1:
                    contador.append(0)
            elif letter == "]":
                group -= 1
            elif letter == ",":
                condicion_guardar = [-100,-100,-100]
                for condicion_guardar in numero_guardar:
                    if contador[group] == condicion_guardar[0] and group == condicion_guardar[1]:
                        if condicion_guardar[2] == -1:
                            guardar = False
                        elif condicion_guardar[2] > -1:
                            guardar = True
                        break
                orden_exec = ""
                pos_exec = ""
                list_exec = []
                for c in range(group):
                    pos_exec += str("[" + str(contador[c]) + "]")
                    list_exec.extend(contador[c])
                orden_exec += str(".append(valor)")  
                end_while = False
                while not end_while:                    
                    try:
                        printf("exec. final" + str(pos_exec) + str(orden_exec) , 2)
                        printf("valor: " + str(valor), 2)
                        exec(str("final"+pos_exec+orden_exec))
                        end_while = True
                    except IndexError:
                        order = ""
                        for a in list_exec:
                            oreder += "[" + a + "]" 
                            exec("final" + order + ".extend([])")

                if guardar == True:
                    printf("Guardado " + str(valor),3)
                    exec(str("final_return"+orden_exec))
                if condicion_guardar[2] == 0:
                    guardar = False
                valor = ""
            elif letter == "$":
                if group >= 0:
                    marcapaginas_antes = contador - 1
                else:
                    marcapaginas_lista.append([[marcapaginas_antes,contador+1],group*-1])
                    for condicion_guardar2 in marcapaginas_guardar:
                        if condicion_guardar2[0] == marcapaginas_valor:
                            if condicion_guardar2[1] == -1:
                                guardar = False
                            elif condicion_guardar2[1] == 1:
                                guardar = True
                            marcapaginas_valor = ""
                            break
                group *= -1
            else:
                if group > 0:
                    valor += str(letter)
                else:
                    marcapaginas_valor += str(letter)
            contador[group] += 1
    printf("Fichero leído! ", 1)
    printf("Resultado: " + str(final_return), 3)
    return final_return
        

def guardar_fichero(path, lista):
    abrir_archivo(path,"w")
    archivo = abrir_archivo(path,"a")
    lista_guardar = simplificar_lista(lista)
    write_this = ""
    for elemento in lista_guardar:
        if elemento == "]" and write_this[len(write_this)-1] == ",":
            write_this = write_this[0:(len(write_this)-1)]
        write_this += str(elemento)
        if not elemento == "[" and not elemento == "]":
            write_this += (",")
    archivo.write(write_this)
    archivo.close()

    


def encontrar_fichero(path, busqueda):
    #encuentra un valor o texto en el archivo guardado. Devuelve valor y posicion. Si hay mas de uno, devuelve lista de listas
    path = str(path)
    printf("Funcion encontrar_fichero(" + str(path) +"," + str(busqueda)+")",2)
    lista_final = []
    contador = 0
    lista_busqueda = simplificar_lista(leer_fichero(path,"-"))
    printf(str(lista_busqueda),3)
    for valor_guardado in lista_busqueda:
        printf("Probando el valor " + str(valor_guardado),3)
        if valor_guardado == busqueda:
            lista_final.append([valor_guardado, contador])
            printf("Encontrado valor " + str(valor_guardado) + " en la posicion " + str(contador),2)
        else:
            printf(str(valor_guardado) + " != " + str(busqueda), 3)
        contador += 1
    printf("lista_final = " + str(lista_final),3)
    return lista_final

def simplificar_lista(lista):
    out = []
    for elemento in lista:
        if hasattr(elemento,'__iter__'):
            out.extend("[")
            out.extend(simplificar_lista(elemento))
            out.extend("]")
            printf("out: " + str(out), 3)
        else:
            out.append(elemento)
    printf("out_return: " + str(out), 2)
    return out

def existe_fichero(path):
    if os.path.exists(path):
        return True
    else:
        return False

guardar_fichero(path_registro+"test.txt", [1,2,30,[4,5,6,[7,8,9,[1,2]]]])
print(encontrar_fichero(path_registro+"test.txt", 4))
print("fin")