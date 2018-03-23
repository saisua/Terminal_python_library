#/bin/env python
import os
import sys
import socket
import urllib.request
import select
import collections

"""
os.system("python3 -m pip install pybluez")
import bluetooth
"""

######
#Poner en el mismo directorio y:
#sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath("Library.py"))))
#from Library import *
#set_external_file(os.path.dirname(os.path.abspath("Myextfile")),"Myextfile")
######

path_registro = str(os.getcwd()) + chr(92)
argumentos = sys.argv
verbose = 3
lista_argumentos = []

client_socket = None

def set_external_file(path,filename):
    external_file = str(path)
    sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath("Library.py"))))
    exec("import "+str(filename)+" as extfile")

def printf(printed,verb):
    if verbose >= verb:
        print(printed)


printf("",1)
printf("",1)
printf("",1)
printf("",1)
printf("",1)
printf("",1)

def tclient(list):
    print("funcion tclient("+str(list)+")")
    Int_client(str(list[0]),list[1])

def Int_client(host, port):
    global server, client_socket
    printf("funcion client(" + str(host) + "," + str(port)+")",2)
    server=""
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    printf("Server = " + str(server),3)
    conexion = False
    acceder = "no"
    while not conexion:
        try:
            printf("Server_ip = " + str(host) + ", port = " + str(port),1)
            if host[0] == "'":
                host = host[1:len(host)-1]
            server.connect((str(host),int(port)))
            printf("Se ha establecido conexion correctamente con " + str(host),0)
            conexion = True
            acceder = "y"
        except:
            printf("No se ha podido conectar con el servidor",0)
            r = preguntar("Reintentar conexion? Y/n/forzar")
            if r == "forzar" or r == "Forzar" or r == "FORZAR":
                conexion = True
                acceder = "y"
            elif not si_o_no(r):
                break
            pass
    tiempo_espera = 10
    tiempo_espera_inicial = tiempo_espera
    printf("Tiempo de espera = " + str(tiempo_espera),2) 
    if si_o_no(acceder):
        printf("Instrucciones al servidor:",0)
        data = ""
        continuar = False
        while True:
            if tiempo_espera <= tiempo_espera_inicial or not continuar:
                r = preguntar_din() 
            if r == "exit":
                break
            elif r != "":
                data = sendtoserver(r,host,port)
                r = ""
            server.settimeout(tiempo_espera)
            try: 
                data_coded = server.recv(1024)
                data = data_coded.decode("utf-8")
                printf("El servidor ha respondido: " + str(data), 1)
                tiempo_espera = tiempo_espera_inicial
                printf("Tiempo de espera = " + str(tiempo_espera),2) 
            except socket.timeout:
                printf("El servidor ha agotado el tiempo de espera.",0)
                if tiempo_espera == tiempo_espera_inicial:    
                    resp = preguntar("Cerrar conexion? Y/n/'R'eintentar/'C'ontinuar")    
                    if resp == "n" or resp == "N" or resp == "no" or resp == "No" or resp == "NO":
                        tiempo_espera += 1
                        printf("Se ha aumentado el tiempo de espera a " + str(tiempo_espera),1)
                    elif resp == "reintentar" or resp == "Reintentar" or resp == "REINTENTAR" or resp == "r" or resp == "R": 
                        continuar = True
                        tiempo_espera += 1
                        printf("Se ha aumentado el tiempo de espera a " + str(tiempo_espera),1)
                    elif resp == "continuar" or resp == "Continuar" or resp == "CONTINUAR" or resp == "c" or resp == "C":
                        continue
                    else:
                        close_server()
                        break
                else:
                    tiempo_espera += 1
                    printf("Se ha aumentado el tiempo de espera a " + str(tiempo_espera),1)
            if data != "" and data != None:
                printf("El servidor responde: " + str(data),0)
                data = ""

def sendtoserver(message,address,port):
    global server, client_socket
    printf("Funcion sendtoserver("+str(message)+","+str(address)+","+str(port)+")",2)
    try:
        server.sendto(bytearray(str(message),"utf-8"),(str(address),int(port)))
        printf("Enviado mensaje: " + str(message),2)
        printf("Enviado mensaje codificado:" + str(bytearray(message,"utf-8")),3)
    except:
        printf("Ha habido un error. Esta el servidor visible?",0)
        return -1

def sendtoall(message):
    global server, client_socket
    printf("Funcion sendtoall("+str(message)+","+str(client_socket)+")",2)
    try:
        client_socket.sendall(bytearray(message,"utf-8"))
        printf("Enviado mensaje: " + str(message),3)
    except:
        printf("Ha habido un error. Esta el receptor visible?",0)
        return -1

def sendtoclient(message,address):
    global server, client_socket
    printf("Funcion sendtoclient("+str(message)+","+ str(address)+")",2)
    try:
        client_socket.send(bytearray(message,"utf-8"),address)
        printf("Enviado mensaje: " + str(message),3)
    except:
        printf("Ha habido un error. Esta el cliente visible?",0)
        return -1
        
def sendfiletoserver(path):
    global server, client_socket
    #NOT TESTED
    printf("Funcion sendfiletoserver("+str(path)+")",2)
    try:
        server.sendfile(path,0,None)
    except:
        printf("Ha habido un error. Esta el servidor visible?",0)
        return -1

def sendfiletoall(path):
    global server, client_socket
    #NOT TESTED
    printf("Funcion sendfiletoall("+str(path)+")",2)
    try:
        client_socket.sendfile(path,0,None)
    except:
        printf("Ha habido un error. Esta el cliente visible?",0)
        return -1

def Int_server():
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
    cliente_connected = []
    cliente_Noresponse = collections.Counter()
    try:
        (client_socket0, address0) = server.accept()
        cliente_connected.append(cliente)
        exec("printf('Cliente"+str(cliente)+": ' + str(address"+str(cliente)+"),1)")
        printf("Se ha conectado un cliente",0)
    except socket.timeout:
        printf("Se ha acabado el tiempo máximo de espera.",0)
    data = ""
    r = ""
    free_will = False
    printf("Buscando otros clientes...",3)
    while True:
        try:
            cliente += 1
            server.settimeout(.1)
            server.listen(0)
            exec("client_socket"+str(cliente)+", address"+str(cliente)+" = server.accept()")
            exec("printf('Cliente"+str(cliente)+": ' + str(address"+str(cliente)+"),1)")
            cliente_connected.append(cliente)
            pass
        except socket.timeout:
            cliente -= 1
            if free_will == True:
                r = preguntar_din()
            for clientes in cliente_connected:  
                cliente_socket = eval("client_socket"+str(clientes)) 
                cliente_socket.settimeout(3)
                try:
                    data = cliente_socket.recv(1024).decode('utf-8')
                    if data == None:
                        cliente_Noresponse.update({str(clientes):1})
                        printf("El cliente" + str(clientes) + " ha enviado None (x" + str(cliente_Noresponse[str(clientes)])+")",3)
                        if cliente_Noresponse[str(clientes)] > 10:
                            printf("Parece que el cliente"+str(clientes)+ " se ha desconectado. Cerrando conexion...",1)
                            cliente_connected.remove(clientes)
                            del cliente_Noresponse[str(clientes)]
                            exec("client_socket"+str(clientes)+".close()")
                            continue
                except:
                    pass
                if str(data) != "" and str(data) != None:    
                    printf("Recibido mensaje: " + str(data),3)
                    exec("client_socket"+str(clientes)+".settimeout(3)")
                    response = try_execute(data)
                    if not response:
                        printf("Parece que no se devuelve respuesta. response = -1",3)
                        response = -1
                    try:
                        try:    
                            err = eval("sendtoall(str(response),client_socket"+str(clientes)+")")
                            if err != -1:    
                                printf("Enviada informacion de vuelta: " + str(response) + " a cliente" + str(clientes),3)
                            data = ""
                        except:
                            printf("Ha ocurrido algun tipo de error",2)
                            pass
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
        except KeyboardInterrupt:
            for clientes in cliente_connected:
                exec("client_socket"+str(clientes)+".close()")
            close_server()
            printf("Conexión cerrada correctamente",0)

    #Cerrar socket primero, pues socket pertenece a server
    for clientes in cliente_connected:
        exec("client_socket"+str(clientes)+".close()")
    close_server()
    printf("Conexión cerrada correctamente",0)

def try_execute(data):
    global server, client_socket, server2, client_socket2
    response = None
    printf("funcion try_execute("+str(data)+")",2)
    try:          
        response = eval(data)        
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
    argumento_analizado = ""
    for arg in argumentos[1:]:                   
        arg = str(arg)
        printf("arg = " + str(arg),3)
        if arg[0] == "-":
            if len(lista_final) > 0:
                printf("lista_final = " + str(lista_final),2)
                try:
                    exec(str(argumento_analizado[0][0:len(argumento_analizado[0])-1])+str(lista_final)+")")
                except:
                    exec("extfile."+str(argumento_analizado[0][0:len(argumento_analizado[0])-1])+str(lista_final)+")")
                
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
                try:
                    exec(argumento_analizado[0])
                except:
                    exec("extfile."+str(argumento_analizado[0]))
        elif len(argumento_analizado[1:]) != 0 and len(lista_variables) >= variable_numero:
            if numero_variables < 0:
                #[tipo_argumento,numero_argumentos]
                lista_variables.append(lista_variables[variable_numero])
            if lista_variables[variable_numero][0] != "all":
                try:
                    printf("Try: arg = " + str(lista_variables[variable_numero][0])+"("+str(arg) + ")",2)
                    arg = eval(str(lista_variables[variable_numero][0])+"("+str(arg)+")")
                    arg = cambiar_tipo(arg,str(lista_variables[variable_numero][0]))
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
        try:
            exec(str(argumento_analizado[0][0:len(argumento_analizado[0])-1])+str(lista_final)+")")
        except:
            exec("extfile."+str(argumento_analizado[0][0:len(argumento_analizado[0])-1])+str(lista_final)+")")

def tipo_argumento(arg):
    printf("Funcion tipo_argumento("+str(arg)+")",2)
    arg = str(type(arg))
    arg_type = arg[8:(len(arg)-2)]
    printf(arg_type,2)
    return arg_type

def analizar_argumento(arg, lista_argumentos):
    printf("Funcion analizar_argumento(" + str(arg) + "," + str(lista_argumentos) + ")",2)
    funcion_ejecutar = ""
    tipo_de_argumento = ""
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
                printf("tipo_de_argumentos = " + str(tipo_de_argumento) + ", numero_argumentos = " + str(numero_argumentos),3)
                if letter == "(":
                    argumento = True
                    funcion_ejecutar += letter
                elif letter == ")":
                    argumento = False
                    if numero_argumentos >= 0:
                        numero_argumentos += 1
                    if tipo_de_argumento != "" :
                        lista_return.append([tipo_de_argumento,numero_argumentos])
                        printf("lista_return = " + str(lista_return),2)
                    if numero_argumentos < 0:
                        break
                    numero_argumentos = 0
                    tipo_de_argumento = ""
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
                        if tipo_de_argumento != "":
                            printf("Añadido argumento: "+ str([tipo_de_argumento,numero_argumentos]),2)
                            lista_return.append([tipo_de_argumento,numero_argumentos])
                        if numero_argumentos < 0:
                            break
                        numero_argumentos = 0
                        tipo_de_argumento = ""
                        numero = False
                    elif letter == ":":
                        numero_argumentos = -1
                        tipo_de_argumento = "all"
                        printf("Encontrado '"+str(letter)+"'. > numero_argumentos = " + str(numero_argumentos) + ", tipo_argumento = " + str(tipo_de_argumento),2)
                    elif letter == ";":
                        numero_argumentos = -1
                        printf("Encontrado '"+str(letter)+"'. > numero_argumentos = " + str(numero_argumentos),2)
                    elif letter == "$":
                        tipo_de_argumento = "all"
                        printf("Encontrado '"+str(letter)+"'. > numero_argumentos = " + str(numero_argumentos),2)
                    elif letter == "@" and tipo_de_argumento != "all":
                        tipo_de_argumento = "str"
                        printf("Encontrado '"+str(letter)+"'. > numero_argumentos = " + str(numero_argumentos),2)
                    elif letter == "*" and tipo_de_argumento != "all":
                        tipo_de_argumento = "int"
                        printf("Encontrado '"+str(letter)+"'. > numero_argumentos = " + str(numero_argumentos),2)
                    elif letter == "?" and tipo_de_argumento != "all":
                        tipo_de_argumento = "bool"
                        printf("Encontrado '"+str(letter)+"'. > numero_argumentos = " + str(numero_argumentos),2)
                    elif letter == "." and tipo_de_argumento != "all":
                        tipo_de_argumento = "float"
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
        printf("Parece que ya son del mismo tipo",2)
        return arg
    else:
        if tipo == "str":
            try:
                arg = str(arg)
                tipo_argumento(arg)
                return arg
            except:
                pass
        elif tipo == "int":
            try:
                arg = int(arg)
                tipo_argumento(arg)
                return arg
            except:
                pass
        elif tipo == "float" or tipo == "flo":
            try:
                arg = float(arg)
                tipo_argumento(arg)
                return arg
            except:
                pass
        elif tipo == "bool" or tipo == "boo":
            try:
                arg = bool(arg)
                tipo_argumento(arg)
                return arg
            except:
                pass
    return arg

def abrir_archivo(path,modo, others=""):
    printf("Abriendo archivo " + str(path), 1)
    if modo == "r" or modo == "w" or modo == "a" or modo == "r+":
        printf("Modo aceptado " + str(modo), 2)
        if existe_fichero(path):
            archivo = open(path, modo)
            printf("archivo: " + str(archivo),3)
            if modo != "w" and modo != "a":
                if others == "l":
                    archivo_abierto = archivo.readlines()
                else:
                    archivo_abierto = archivo.read()
                printf("archivo abierto: " + str(archivo_abierto),2)
                return archivo_abierto
            return archivo
        else:
            printf("ERROR: el archivo " + str(path) + " no existe", 0)
            printf("",0)
            inp = preguntar("Crear ahora? Y/n: ")
            if si_o_no(inp):
                printf("Creando " + str(path),1)
                open(path, modo)
                printf("Archivo creado!",1)
                inp = preguntar("Probar a abrir " + str(path) + "? Y/n:")
                if si_o_no(inp):
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
    printf("funcion leer_fichero(" + str(path) + "," + str(cantidad) + ")",2)
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
    marca_control = 0


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
                if anterior == -1:
                    marcapaginas_guardar.append(["$" + marcapaginas_valor + "$",1])
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
        elif letter == "]":
            group -= 1
            valor = ""
        elif letter == "," or (letter == "]" and valor != ""):
            marca_control = 0
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
                    pos_exec += str("[" + str(contador[c]-1) + "]")
                    list_exec.append(contador[c])
            orden_exec += str(".append(cambiar_tipo(valor[3:],valor[0:3]))")  
            end_while = False
            while not end_while:     
                if len(valor) <= 3:
                    valor = ""
                    break               
                try:
                    if group > 1:
                        printf("exec. final" + str(pos_exec) + str(orden_exec) , 2)
                        printf("valor: " + str(valor), 2)
                        exec(str("final"+pos_exec+orden_exec))
                        if guardar:
                            exec(str("final_return"+pos_exec+orden_exec))
                        else:
                            final_return.append("")
                        #else:
                        #    exec(str("final_return"+pos_exec+".append(None)"))
                    else:
                        exec("final"+orden_exec)
                        if guardar:
                            exec("final_return"+orden_exec)
                        else:
                            final_return.append("")
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
            if marca_control == 0:
                marcapaginas_valor = "$"
                marca_control = 1
            else:
                marca_control = 0
                marcapaginas_valor += "$"
            if group >= 0:
                marcapaginas_antes = contador[group] - 1
            else:
                marcapaginas_lista.append([[marcapaginas_antes,contador[group]+1],group*-1])
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
    if tipo_argumento(cantidad) == "int":
        try:
            final_return = [final_return[cantidad]]
        except:
            return False
    elif tipo_argumento(cantidad) == "list":
        try:
            final_return = eval("final_return" + str(cantidad))
        except:
            return False

    printf("Fichero leído! ", 1)
    printf("Resultado: " + str(final_return), 3)
    #printf("Devolviendo la lista ([valor buscado,posición])",3)
    return final_return
        
def borrar_fichero(path):
    tmp = abrir_archivo(path,"w").close()

def guardar_fichero(path, lista, salto=False):
    archivo = abrir_archivo(path,"a")
    if salto:
        archivo.write("\n")
    lista_guardar = simplificar_lista(lista)
    write_this = ""
    for elemento in lista_guardar:
        printf("elemento: " + str(elemento), 3)
        if elemento == "]" and write_this[len(write_this)-1] == ",":
            write_this = write_this[0:(len(write_this)-1)]
        elif elemento != "[":
            write_this +=  tipo_argumento(elemento)[:3]
        write_this += str(elemento)
        if not elemento == "[" and not elemento == "]":
            write_this += (",")
    archivo.write(write_this)
    archivo.close()

def encontrar_en_fichero(path, busqueda):
    #encuentra un valor o texto en el archivo guardado. Devuelve valor y posicion. Si hay mas de uno, devuelve lista de listas
    path = str(path)
    printf("Funcion encontrar_en_fichero(" + str(path) +"," + str(busqueda)+")",2)
    lista_busqueda = simplificar_lista(leer_fichero(path,"-"))
    printf("Buscando " + str(busqueda) + " en " + str(lista_busqueda),3) 
    lista_final = encontrar_en_lista(lista_busqueda,busqueda)
    return lista_final
  
def encontrar_en_lista(lista, busqueda):
    printf("funcion encontrar_en_lista(" + str(lista) + "," + str(busqueda) + ")",2)
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
            printf("El tipo de variable del elemento de la lista " + str(valor_guardado) + " (" + str(tipo_argumento(valor_guardado)) + ") no coincide con el buscado",2)
    if contador == 0:
        printf("O el archivo esta vacio, o el tipo de variable que se busca (" + str(tipo_argumento(busqueda)) + ") es erróneo",0)

    printf("lista_final = " + str(lista_final),3)
    return lista_final

def simplificar_lista(lista):
    ret = []
    for elemento in lista:
        if tipo_argumento(elemento) == "list":
            ret.extend("[")
            ret.extend(simplificar_lista(elemento))
            ret.extend("]")
            printf("sub-return: " + str(ret), 3)
        else:
            ret.append(elemento)
    printf("return: " + str(ret), 2)
    return ret

def existe_fichero(path):
    if os.path.exists(path):
        return True
    else:
        return False

def si_o_no(respuesta):
    printf("funcion si_o_no(" + str(respuesta) + ")",2)
    if respuesta == "Si" or respuesta == "Sí" or respuesta == "sí" or respuesta == "si" or respuesta == "SÍ" or respuesta == "SI" or respuesta == "S" or respuesta == "s" or respuesta == "Y" or respuesta == "YES" or respuesta == "Yes" or respuesta == "yes" or respuesta == "y":
        return True
    elif respuesta == "No" or respuesta == "NO" or respuesta == "no" or respuesta == "n" or respuesta == "N":
        return False
    else:
        return respuesta

def comparar_archivos(archivo1_path, archivo2_path, exactitud):
    printf("funcion comparar_archivos(" + str(archivo1_path) + ", " + str(archivo2_path) + ", " + str(exactitud)+ ")", 2)
    ###Exactitud = 0, compara archivos abiertos
    ## Exactitud = 1, compara lineas
    #  Exactitud = 2, compara letras
    archivo1 = abrir_archivo(archivo1_path, "r", "l")
    archivo2 = abrir_archivo(archivo2_path, "r", "l")

    if exactitud == 0:
        if archivo1 == archivo2:
            printf("Archivo1 = Archivo2" , 1)
            return True
        else:
            printf("Archivo1 != Archivo2" , 2)
            return False
    elif exactitud >= 1:
        archivo1_lineas = archivo1
        archivo1_lineas = [x.strip() for x in archivo1_lineas] 
        archivo2_lineas = archivo2
        archivo2_lineas = [x.strip() for x in archivo2_lineas] 

        archivo2_comparado = archivo2_lineas
        contador1 = -1
        lineas1_incorrectas = []

        for linea1 in archivo1_lineas:
            contador1 += 1
            contador2 = -1
            correcto = False
            for linea2 in archivo2_comparado:
                contador2 += 1
                if linea1 == linea2:
                    archivo2_comparado.pop(contador2)
                    correcto = True
                    break
            if correcto == False:
                lineas1_incorrectas.append(contador1)
                
                

        if exactitud == 2:
            ##Letras1_incorrectas[[linea,posicion]]
            letras1_incorrectas = []
            

            for linea1 in lineas1_incorrectas:
                contador = -1
                for letra1 in str(archivo1_lineas[linea1]):
                    contador += 1
                    for linea2 in archivo2_comparado:
                        if contador < len(linea2):
                            if letra1 != str(linea2[contador]):
                                letras1_incorrectas.append([linea1,contador])
                        else: 
                            letras1_incorrectas.append([linea1,contador])
            printf("Encontradas letras incorrectas: " + str(letras1_incorrectas),3)
            return letras1_incorrectas
        else:
            printf("Encontradas lineas incorrectas: " + str(lineas1_incorrectas),3)
            return lineas1_incorrectas
    else:
        printf("Error en el valor de exactitud. Devolviendo False", 1)
        return False

test1 = "C://Users//Pat//Desktop//test1.txt"
test2 = "C://Users//Pat//Desktop//test2.txt"

borrar_fichero(test1)
borrar_fichero(test2)
guardar_fichero(test1, ["hola", 2, "$aa$", [34,"$ee$"], 34] )

leer_fichero(test1,"-$aa$")

"""
def bt_server(bt_addr):
    server_sock=bluetooth.BluetoothSocket( bluetooth.L2CAP )
    
    port = 0x1001

    server_sock.bind(("",port))
    server_sock.listen(0)

    client_sock,address = server_sock.accept()
    print("Accepted connection from ",address)

    data = client_sock.recv(1024)
    print("Data received: ", str(data))

    while data:
        client_sock.send('Echo => ' + str(data))
        data = client_sock.recv(1024)
        print("Data received:", str(data))
    
    client_sock.close()
    server_sock.close()

def bt_client(bt_addr):
    sock=bluetooth.BluetoothSocket(bluetooth.L2CAP)
    
    port = 0x1001

    print("trying to connect to %s on PSM 0x%X" % (bt_addr, port))

    sock.connect((bt_addr, port))

    print("connected.  type stuff")
    while True:
        data = input()
        if(len(data) == 0): break
        sock.send(data)
        data = sock.recv(1024)
        print("Data received:", str(data))

    sock.close()

def bt_scan():
    services = bluetooth.find_service(address=None)

    if len(services) > 0:
        print("found %d services on %s" % (len(services), sys.argv[1]))
        print("")
    else:
        print("no services found")

    for svc in services:
        print("Service Name: %s"    % svc["name"])
        print("    Host:        %s" % svc["host"])
        print("    Description: %s" % svc["description"])
        print("    Provided By: %s" % svc["provider"])
        print("    Protocol:    %s" % svc["protocol"])
        print("    channel/PSM: %s" % svc["port"])
        print("    svc classes: %s "% svc["service-classes"])
        print("    profiles:    %s "% svc["profiles"])
        print("    service id:  %s "% svc["service-id"])
        print("")

bt_scan()
"""

read_arg(argumentos,lista_argumentos)