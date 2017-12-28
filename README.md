# Terminal_python_library
#README

####  HOW TO IMPORT THIS LIBRARY INTO YOUR OWN PROGRAM:
### Once Library.py is in the same as your program:
##
#sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath("Library.py"))))
#from Library import *
#set_external_file(os.path.dirname(os.path.abspath("Myextfile")),"Myextfile")
##
### If you want Library.py in another path, just change sys.path.append(os.path.abspath("Library_path"))
#####

####Info per function:

#def set_external_file(path,fliename)
#
#If you want to be able to run my full library, this is a must-run function, which has to be run at the beginning
#
#Arguments:
#path is the path to your file, and filename is the name of your own program, without the '.py'

#def printf(printed,verb):
#
#Only do print(printed) if verb >= verbosity
#
#Arguments:
#printed is the message to be printed, and verb is the minimum level of verbosity needed to be displayed

#def client(host, port):
#
#Tries to connect via socket-server connection to a remote server.
#
#Arguments:
#host is the ip (either localhost, local ip or public ip) where try to connect, and port is the port where the connection will be made (default 42680)

#def sendtoserver(message,address,port), sendtoall(message,client_socket), sendtoclient
#
#Just send a message to the client or to the server
#
#Arguments:
#message is a str, the one which will be sent to the server/client, address is the ip and port is the port (not yours) 
#client_socket is the result of "(client_socket, address) = server.accept()"

#def sendfiletoserver(path), sendfiletoall
#
#Untested feature, i don't even know if that works properly. I don't need it yet
#
#Arguments:
#path is the path to the file is being sent

#def server()
#
#Just run it and watch people connect to you! (if you programed so)
#If variable free_will == True, server does acl like a client, but it won't receive any message while the operator does not send anything to all clients, so not so useful
#

#def try_execute(data):
#
#Tries to execute data, first on python, then in your os. Be careful you let in
#
#Arguments:
#data is the command the program is going to try execute. And... boom! you have a trojan (a pretty bad one)

#def close_server():
#
#Shuts down the server. If you are the server, it is recommended to shut down all sockets first. do it with:
#for clientes in cliente_connected:
   #exec("client_socket"+str(clientes)+".close()")

#def read_arg(argumentos, lista_argumentos):
#
#It does read all arguments given in the terminal, and execute lista_argumentos[argument][1]
#It only does work in your own program if you execute set_external_file(path,fliename) first!!!!
#
#Arguments:
#argumentos is the list of arguments given to the program in the terminal. The first one is a "-.py" str. The program will look for the argument given in lista_argumentos. lista_argumentos if the list of [["-argument","function_to_execute(:)"], ...]
#function_to_execute works this way. Between ():
                    
                    #["-argument", "function_to_execute(asked_variables)"]

                    #"@" One variable type string

                    #"*" One variable type int

                    #"." One variable type float

                    #"?" One variable type boolean

                    #"$" One variable type whatever

                    #":" All variables are type whatever

                    #";@" All variables are type string

                    #"2-4*" Two to Four variables are type int ###NOT WORKING

                    #"," It does split two asked_variables
                   

#def analizar_argumento(arg, lista_argumentos):
#
#Works with read_arg, and only translates the arguments given in a way read_arg can understand them
#
#Arguments:
#arg is the argument(only one) that's being analyzed and lista_argumentos is the same above

#def def cambiar_tipo(arg, tipo):
#
#I'm not proud of this function, it was a home made function which i really don't need. Probably i will remove it and i'll forget i had written this, so this probably will remain here, showing the few bots will ever reach this library my shame
#
#Arguments:
#arg is the argument given, and tipo is the type it should be. The same can be done with whis line of code, i thought later:
#arg = eval(str(tipo)+"("+str(arg)+")")
#It works because of the way analizar_argumento returns tipo

#def tipo_argumento(arg):
#
#A very simple function, which returns the string that returns type(arg), but without all that unnecessary info to the end-user
#
#Arguments:
#arg is the variable which type is being returned

#def abrir_archivo(path,modo):
#
#Opens the file whith the mode (w,r,a,r+) indicated
#
#Arguments:
#path is the path of the file is being opened, and modo, the way it will be opened, being w = write, r = read, a = append and r+ = read + write

#def preguntar(pregunta):
#
#Asks the user for something and waits for the response
#
#Arguments.
#Pregunta is the question is being asked (i used print, not printf), as i thought i would always ask for something

#def preguntar_din():
#
#It is supposed to be preguntar, but whithout waiting for the user to answer, because is being run in a While or some loop like that. Actually it does not work, you can say it is work on progress
#

#def leer_fichero(path, cantidad):
#
#It does read a file, but only what you tell him. (I don't remember if that worked)
#
#Arguments:
#path is the path of the file is being read, and cantidad is the str which tells the function which lists read. Use "-" to read all the file. Otherwise, there it is, how you know 

    #"1,2,-3 3-6,1 $hello$-"
    
    #From the first group, in the second subgroup, from first to 3rd data 
    #also, from 3rd group to 6th, every 1st subgroup
    #and, finally, form bookmark $hello$ to the end of the file
    
#def guardar_fichero(path, lista):
#
#It only saves lista into a new file
#
#Arguments:
#path is the path where the file is going to be saved. Lista is the list is being saved in it

#def encontrar_en_fichero(path, busqueda):
#
#It only does open a file in path and then executes encontrar_en_lista(lista, busqueda):
#
#Arguments:
#path is the path of the file is being read, and busqueda is the str what encontrar_en_lista will be looking for

#def encontrar_en_lista(lista, busqueda):
#
#It does find anything on any list. Useful
#
#Arguments:
#lista is the list where the function will be looking for busqueda

#def simplificar_lista(lista):
#
#It does insert any subgroup in the main group.
#
#Arguments:
#llista is the list the function will work with. If, for example, my lista = [1,2,[3,4,[5]]], simplificar_lista will return [1,2,3,4,5]

#def existe_fichero(path):
#
#Easy to understand, it does return Ture, if the file does exist. Otherwise, it returns False. 
#
#Arguments:
#path (again) is the path of the file the function will look at to find out if the file does exist or doesn't

#def si_o_no(respuesta):
#
#I was annoyed for writting "y/Y/Yes/yes/YES.........." so i decided to put it in one useless function, but worth for me. Oh, yes, it does return true if respuesta if anything near Yes, and False if it is near No. If it can't find it out, it does return respuesta.
#
#Arguments:
#respuesta should be "respuesta = pregunta('Are you tired of writting this README? (Y/Y)')", so that you can execute

if si_o_no(respuesta):
  close_readme()
--------------------------------------------------------------
saisua got TIMEDOUT (x0)
saisua got TIMEDOUT (x1)
saisua got TIMEDOUT (x2)
saisua got TIMEDOUT (x3)
saisua got TIMEDOUT (x4)
saisua got TIMEDOUT (x5)
saisua got TIMEDOUT (x6)
saisua got TIMEDOUT (x7)
saisua got TIMEDOUT (x8)
saisua got TIMEDOUT (x9)
saisua got TIMEDOUT (x10)
saisua got TIMEDOUT (x11)
Looks like saisua disconnected. Shutting down connection...
completed.
