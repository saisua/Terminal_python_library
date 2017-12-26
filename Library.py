#/bin/env python
import os
import sys
import socket
import urllib.request
import select

path_registro = str(os.getcwd()) + chr(92)
argumentos = sys.argv
verbose = 3
lista_argumentos = [["--hh","ejecutar(@;)"],["--close","close_server()"],["-s","sendtoall(@)"],["--server","server()"],["-c","tclient(@,*)"],["-h", "print(@)"], ["--suma", "sumar(;*)"], ["-a", "anadir(:)"],["-r", "restar(*,.)"],["-m", "multiplicar(2-4*)"]]

###
def sumar(lista):
    print("funcion sumar("+str(lista)+")")
    resultado = 0
    for numero in lista:
        resultado += numero
    print("sumar: "+ str(resultado))

def anadir(lista):
    print("funcion anadir("+str(lista)+")")
    resultado = ""
    for elemento in lista:
        resultado += str(elemento)
    print("anadir: " + str(resultado))

def restar(lista):
    print("funcion restar("+str(lista)+")")
    resultado = lista[0] - lista[1]
    print("restar: " + str(resultado))

def multiplicar(lista):
    print("funcion multiplicar("+str(lista)+")")
    resultado = 1
    for elemento in lista:
        resultado *= elemento
    print("multiplicar: " + str(resultado))

def ejecutar(orden):
    print("funcion ejecutar("+str(orden)+")")
    for a in orden:
        printf("a = " + str(a[1:len(a)-1]),3)
        try:
            exec(str(a[1:len(a)-1]))
        except:
            print("Error ejecutando la orden " + str(a[1:len(a)-1]))
            pass
###

def help():
    print("Esta libreria esta hecha en y para Python"
    "#['-argumento', 'función_a_ejecutar(variables)']"
    "#'@' Variable de tipo String"
    "#'*' Variable de tipo int"
    "#'.' Variable de tipo double o long"
    "#'?' Variable de tipo boolean"
    "#'$' variable del tipo que sea"
    "#':' Todas las variables sean del tipo que sean"
    "#';@' Todas las variables del tipo string"
    "#'2-4*' Dos a cuatro variables de tipo entero"
    "#',' Separa dos condiciones")


def printf(printed,verb):
    if verbose >= verb:
        print(printed)

def tclient(list):
    print("funcion tclient("+str(list)+")")
    client(str(list[0]),list[1])

def client(host, port):
    global server, client_socket
    printf("funcion client(" + str(host) + "," + str(port)+")",2)
    server=""
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    printf("Server = " + str(server),3)
    acceder = "no"
    conexion = False
    while not conexion:
        try:
            print("Server_ip = " + str(host) + ", port = " + str(port))
            if host[0] == "'":
                host = host[1:len(host)-1]
            server.connect((str(host),int(port)))
            #server2.bind((host,port+1))
            #server2.listen(0)
            printf("Se ha establecido conexion correctamente con " + str(host),0)
            conexion = True
            acceder = "y"
        except:
            printf("No se ha podido conectar con el servidor",0)
            r = preguntar("Reintentar conexion? Y/n/forzar")
            if r == "forzar" or r == "Forzar" or r == "FORZAR":
                conexion = True
                acceder = "y"
            elif r == "n" or r == "N" or r == "no" or r == "No" or r == "NO":
                break
            pass
    if acceder == "y" or acceder == "Y" or acceder == "yes" or acceder == "Yes" or acceder == "YES":    
        printf("Instrucciones al servidor:",0)
        data = ""
        while True:
            r = preguntar_din() 
            if r == "exit":
                break
            elif r != "":
                data = sendtoserver(r)
                r = ""
            data = server.recv(1024).decode("utf-8")
            if data != "":
                printf("El servidor responde: " + str(data),0)
                data = ""


def sendtoserver(message):
    global server, client_socket
    try:
        server.sendall(bytearray(message,"utf-8"))
        printf("Enviado mensaje: " + str(message),3)
    except:
        printf("Ha habido un error. Esta el servidor visible?",0)
        pass

def sendtoall(message):
    global server, client_socket
    try:
        client_socket.sendall(bytearray(message,"utf-8"))
        printf("Enviado mensaje: " + str(message),3)
    except:
        printf("Ha habido un error. Esta el receptor visible?",0)
        pass

def sendtoclient(message,address):
    global server, client_socket
    try:
        client_socket.sendto(bytearray(message,"utf-8"),address)
        printf("Enviado mensaje: " + str(message),3)
    except:
        printf("Ha habido un error. Esta el cliente visible?",0)
        pass

def sendfiletoserver(path):
    global server, client_socket
    server.sendfile(path,0,None)

def sendfiletoall(path):
    global server, client_socket
    client_socket.sendfile(path,0,None)

def server():
    global server, client_socket
    printf("funcion server()",2)
    host=""
    port=42680
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server2=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    printf("Intentando establecer el servidor",1)
    printf("Servidor en:",0)
    local_ip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
    printf("Local ip (LAN): "+ str(local_ip),-3)
    public_ip = str(urllib.request.urlopen('http://ip.42.pl/raw').read())
    public_ip = public_ip[2:len(public_ip)-1]
    printf("Public ip: " + public_ip,-3)
    printf("Port = " + str(port),-3)

    server.bind((host,port))
    server.listen(0)
    server.settimeout(20)
    cliente = 0
    try:
        (client_socket0, address0) = server.accept()
        cliente = 1
        printf("Se ha conectado un cliente",0)
        printf("Cliente: " +str(address0),1)
    except socket.timeout:
        printf("Se ha acabado el tiempo máximo de espera.",0)
    data = ""
    r = ""
    free_will = False
    printf("Buscando otros clientes...",3)
    while True:
        try:
            server.settimeout(.1)
            server.listen(0)
            exec("(client_socket"+str(cliente)+", address"+str(cliente)+") = server.accept()")
            exec("printf('Cliente: ' + str(address"+str(cliente)+"),1)")
            cliente += 1
            pass
        except socket.timeout:
            #printf("TIMEOUT",3)
            if free_will == True:
                r = preguntar_din()
            for clientes in range(cliente):    
                exec("data=client_socket"+str(clientes)+".recv(1024).decode('utf-8')")
                #data = server.recv(1024)
                if str(data) != "":    
                    printf("Recibido mensaje: " + str(data),3)
                    response = try_execute(data)
                    if not response:
                        printf("Parece que no se devuelve respuesta. response = -1",3)
                        response = -1
                    try:
                        exec("sendtoclient(response,address"+str(clientes)+")")
                        printf("Enviada informacion de vuelta: " + str(response) + " a cliente " + str(clientes),3)
                        data = ""
                    except:
                        printf("No se ha podido contestar al cliente",0)
                        pass
            if r == "exit":
                break
            elif r != "":
                sendtoall(r)
            pass
        except socket.error:
            printf("Error: Socket error",0)
            break
    close_server()
    client_socket.close()
    printf("Conexión cerrada correctamente",0)

def try_execute(data):
    global server, client_socket, server2, client_socket2
    response = None
    printf("funcion try_execute("+str(data)+")",2)
    try:          
        response = exec(data)        
        printf("Ejecutado en python " + str(data),2)
    except:
        try:
            response = os.system(str(data))
            printf("Ejecutado en el sistema " + str(data),2)
        except:
            pass
        pass
    return response

def close_server():
    global server
    try:
        server.shutdown()
        printf("Parece que el servidor se ha cerrado correctamente",1)
    except:
        printf("Ha habido un error. Esta el servidor abierto?",0)
        pass    
    try:
        server.close()
    except:
        pass

def read_arg(argumentos, lista_argumentos):
    printf("Funcion read_arg(" + str(argumentos) +","+str(lista_argumentos)+")",2)
    lista_variables = []
    variable_numero = 0
    numero_variables = 0
    parametros_final = ""
    lista_final = []
    for arg in argumentos[1:]:                   
        arg = str(arg)
        printf("arg = " + str(arg),3)
        if arg[0] == "-":
            if len(lista_final) > 0:
                printf("lista_final = " + str(lista_final),2)
                exec(str(argumento_analizado[0][0:len(argumento_analizado[0])-1])+str(lista_final)+")")
                parametros_final = ""
                lista_final = []
            numero_variables = 0
            variable_numero = 0
            #analiza determina el argumento a dar, y que variables esperar
            argumento_analizado = analizar_argumento(arg, lista_argumentos)
            printf("Argumento analizado: " + str(argumento_analizado),1)
            if len(argumento_analizado) > 1:
                if argumento_analizado[1] != []:
                    printf("Se han detectado " + str(len(argumento_analizado[1:])) + " argumentos",2)
                    lista_variables = (argumento_analizado[1:])
                    for argumento in argumento_analizado[1:]:
                        if numero_variables >= 0:
                            numero_variables += int(argumento[1])
            else:
                printf("Parece que no hay argumentos. Ejecutando " + str(argumento_analizado[0]),1)
                exec(argumento_analizado[0])
        elif len(argumento_analizado[1:]) != 0 and len(lista_variables) >= variable_numero:
            if numero_variables < 0:
                #[tipo_argumento,numero_argumentos]
                lista_variables.append(lista_variables[variable_numero])
            if lista_variables[variable_numero][0] != "all":
                try:
                    printf("Try: arg = " + str(lista_variables[variable_numero][0])+"("+str(arg) + ")",2)
                    cambiar_tipo(arg,str(lista_variables[variable_numero][0]))
                except:
                    printf("Parece que el tipo de argumento no coincide. Puede que haya errores.",1)
                    pass
            tipo = tipo_argumento(arg)
            printf("lista_variables = " + str(lista_variables),2)
            printf("variable_numero = " + str(variable_numero),2)
            if lista_variables[variable_numero][0] == "all" or lista_variables[variable_numero][0] == tipo:
                printf("Tipo = " + str(tipo) + " , " + str(lista_variables[variable_numero][0]),2)
                if tipo == "str":
                    parametros_final += "'"
                    parametros_final += arg
                    parametros_final += "'"
                    lista_final.append(parametros_final)
                    printf("parametros_final = " + str(parametros_final),2)
                else:
                    lista_final.append(arg)
                parametros_final = ""
            variable_numero += 1
    printf("lista_final = " + str(lista_final),2)
    if len(lista_final) > 0:
        exec(str(argumento_analizado[0][0:len(argumento_analizado[0])-1])+str(lista_final)+")")

def analizar_argumento(arg, lista_argumentos):
    printf("Funcion analizar_argumento(" + str(arg) + "," + str(lista_argumentos) + ")",2)
    funcion_ejecutar = ""
    tipo_argumento = ""
    numero_argumentos = 0
    lista_return = []
    numero = False
    asked = ""
    for listed_arg in lista_argumentos:
        if listed_arg[0] == arg:
            printf("Argumento " + str(arg) + " encontrado. Analizando...",1)
            argumento = False
            for letter in listed_arg[1]:
                printf("Letter = " + str(letter),3)
                printf("tipo_argumentos = " + str(tipo_argumento) + ", numero_argumentos = " + str(numero_argumentos),3)
                if letter == "(":
                    argumento = True
                    funcion_ejecutar += letter
                elif letter == ")":
                    argumento = False
                    if numero_argumentos >= 0:
                        numero_argumentos += 1
                    if tipo_argumento != "" :
                        lista_return.append([tipo_argumento,numero_argumentos])
                        printf("lista_return = " + str(lista_return),2)
                    if numero_argumentos < 0:
                        break
                    numero_argumentos = 0
                    tipo_argumento = ""
                    numero = False
                    break
                elif argumento == True:
                    #["-argumento", "función_a_ejecutar(variables)"]
                    #"@" Variable de tipo String
                    #"*" Variable de tipo int
                    #"." variable de tipo double o long
                    #"?" variable de tipo boolean
                    #"$" variable del tipo que sea
                    #":" Todas las variables sean del tipo que sean
                    #";@" Todas las variables del tipo string
                    #"2-4*" Dos a cuatro variables de tipo entero
                    #"," Separa dos condiciones

                    if letter == ",":
                        if numero_argumentos >= 0:
                            numero_argumentos += 1
                        if tipo_argumento != "":
                            printf("Añadido argumento: "+ str([tipo_argumento,numero_argumentos]),2)
                            lista_return.append([tipo_argumento,numero_argumentos])
                        if numero_argumentos < 0:
                            break
                        numero_argumentos = 0
                        tipo_argumento = ""
                        numero = False
                    elif letter == ":":
                        numero_argumentos = -1
                        tipo_argumento = "all"
                        printf("Encontrado '"+str(letter)+"'. > numero_argumentos = " + str(numero_argumentos) + ", tipo_argumento = " + str(tipo_argumento),2)
                    elif letter == ";":
                        numero_argumentos = -1
                        printf("Encontrado '"+str(letter)+"'. > numero_argumentos = " + str(numero_argumentos),2)
                    elif letter == "$":
                        tipo_argumento = "all"
                        printf("Encontrado '"+str(letter)+"'. > numero_argumentos = " + str(numero_argumentos),2)
                    elif letter == "@" and tipo_argumento != "all":
                        tipo_argumento = "str"
                        printf("Encontrado '"+str(letter)+"'. > numero_argumentos = " + str(numero_argumentos),2)
                    elif letter == "*" and tipo_argumento != "all":
                        tipo_argumento = "int"
                        printf("Encontrado '"+str(letter)+"'. > numero_argumentos = " + str(numero_argumentos),2)
                    elif letter == "?" and tipo_argumento != "all":
                        tipo_argumento = "bool"
                        printf("Encontrado '"+str(letter)+"'. > numero_argumentos = " + str(numero_argumentos),2)
                    elif letter == "." and tipo_argumento != "all":
                        tipo_argumento = "float"
                        printf("Encontrado '"+str(letter)+"'. > numero_argumentos = " + str(numero_argumentos),2)
                    else:
                        try:
                            if tipo_argumento(int(letter)) == "int":
                                numero = True
                                numero_argumentos = letter
                                #De momento
                        except:
                            asked += letter
                            pass
                else:
                    funcion_ejecutar += letter

    if listed_arg[1] != "-":
        final = [funcion_ejecutar+")"]
    final.extend(lista_return) 
    printf("Argumento analizado: " + str(arg) + " necesita " + str(lista_return) + " argumentos para poder ejecutar " + str(funcion_ejecutar) + ")",1)
    printf("final = " + str(final),2)
    return final

def cambiar_tipo(arg, tipo):
    if tipo_argumento(arg) == tipo:
        return arg
    else:
        if tipo == "str":
            try:
                arg = str(arg)
                return arg
            except:
                pass
        elif tipo == "int":
            try:
                arg = int(arg)
                return arg
            except:
                pass
        elif tipo == "float":
            try:
                arg = float(arg)
                return arg
            except:
                pass
        elif tipo == "bool":
            try:
                arg = bool(arg)
                return arg
            except:
                pass
    return arg

def tipo_argumento(arg):
    printf("Funcion tipo_argumento("+str(arg)+")",2)
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
            inp = preguntar("Crear ahora? Y/n: ")
            if inp == "Y" or inp == "y":
                printf("Creando " + str(path),1)
                open(path, modo)
                printf("Archivo creado!",1)
                inp = preguntar("Probar a abrir " + str(path) + "? Y/n:")
                if inp == "Y" or inp == "y":
                    abrir_archivo(path,modo)

    else:
        printf("ERROR: modo no permitido: " + str(modo),0)
        printf("Los modos permitidos son:", 0)
        printf("r = read        w = write",0)
        printf("a = append      r+ = read + write",0)

def preguntar(pregunta):
    printf("funcion preguntar(" + str(pregunta)+ ")",2)
    print(pregunta)
    respuesta = ""
    while True:
        respuesta = str(input())
        if respuesta != "":
            printf("respuesta = " + str(respuesta),2)
            break
    return respuesta

def preguntar_din():
    printf("funcion preguntar_din()",2)
    respuesta = ""
    respuesta = str(input())
    if respuesta != "":
        printf("respuesta = " + str(respuesta),2)
        return respuesta

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
                #Falta hacer 3-6 del 3 al 6
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

        marcapaginas_valor = ""
        valor = ""
        group = 1
        contador = [0,0]
        contar = 0

        for letter in archivo:
            if letter == "[":
                group += 1
                while len(contador) < group + 1:
                    contador.append(0)
            elif letter == "]" and valor == "":
                group -= 1
            elif letter == "," or (letter == "]" and valor != ""):
                condicion_guardar = [-100,-100,-100]
                for condicion_guardar in numero_guardar:
                    for condicion_grupo in condicion_guardar[1]:
                        if contador[group] == condicion_guardar[0] and group == condicion_grupo+1:
                            if condicion_guardar[2] == -1:
                                guardar = False
                            elif condicion_guardar[2] > -1:
                                guardar = True
                            break
                orden_exec = ""
                pos_exec = ""
                list_exec = []
                for c in range(group):
                    if c > 0:
                        pos_exec += str("[" + str(contador[c]) + "]")
                        list_exec.append(contador[c])
                orden_exec += str(".append(valor)")  
                end_while = False
                while not end_while:                    
                    try:
                        if group > 1:
                            printf("exec. final" + str(pos_exec) + str(orden_exec) , 2)
                            printf("valor: " + str(valor), 2)
                            exec(str("final"+pos_exec+orden_exec))
                            if guardar:
                                exec(str("final_return"+pos_exec+orden_exec))
                            else:
                                exec(str("final_return"+pos_exec+".append(None)"))
                        else:
                            exec("final"+orden_exec)
                            exec("final_return"+orden_exec)
                        end_while = True
                    except IndexError:
                        order = ""
                        for a in range(len(list_exec)):
                            if a > 0:
                                order += "[" + str(list_exec[a-1]) + "]" 
                                if a+2 == group:
                                    exec("final" + order + ".append([])")
                                    exec("final_return" + order + ".append([])")
                            elif a == 0 and group -2 == 0:
                                final.append([])
                                final_return.append([])

                if guardar == True:
                    printf("Guardado " + str(valor),3)
                if condicion_guardar[2] == 0:
                    guardar = False
                valor = ""
                contador[group] += 1
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
            contar += 1


    printf("Fichero leído! ", 1)
    printf("Resultado: " + str(final_return), 3)
    printf("Devolviendo la lista ([valor buscado,posición])")
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

def encontrar_en_fichero(path, busqueda):
    #encuentra un valor o texto en el archivo guardado. Devuelve valor y posicion. Si hay mas de uno, devuelve lista de listas
    path = str(path)
    printf("Funcion encontrar_en_fichero(" + str(path) +"," + str(busqueda)+")",2)
    lista_final = []
    lista_busqueda = simplificar_lista(leer_fichero(path,"-"))
    printf("Buscando " + str(busqueda) + " en " + str(lista_busqueda),3) 
    encontrar_en_lista(lista_busqueda,str(busqueda))
    
def encontrar_en_lista(lista, busqueda):
    contador = 0
    lista_final = []
    lista_busqueda = lista
    for valor_guardado in lista_busqueda:
        if tipo_argumento(busqueda) == tipo_argumento(valor_guardado):     
            printf("Probando el valor " + str(valor_guardado),3)
            if valor_guardado == busqueda:
                lista_final.append([valor_guardado, contador])
                printf("Encontrado valor " + str(valor_guardado) + " en la posicion " + str(contador),2)
            else:
                printf(str(valor_guardado) + " != " + str(busqueda), 3)
            contador += 1
        else:
            printf("El tipo de variable del elemento de la lista " + str(valor_guardado) + " (" + str(tipo_argumento(valor_guardado)) + ") no coincide con el de la lista",2)
    if contador == 0:
        printf("O el archivo esta vacio, o el tipo de variable que se busca (" + str(tipo_argumento(busqueda)) + "es erróneo",0)

    printf("lista_final = " + str(lista_final),3)
    return lista_final

def simplificar_lista(lista):
    out = []
    for elemento in lista:
        if tipo_argumento(elemento) == "list":
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

read_arg(argumentos,lista_argumentos)
printf("fin",1)
