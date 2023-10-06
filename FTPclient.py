#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  xFTPclient.py
#  

SSIZE = 2048
CHUNK = 512
msgQUIT = "QUIT"
msgDIR = "DIR"
msgGET = "GET"
msgPUT = "PUT"
msgACK = "ACK"
msgOK = "OK"
msgSTART = "START"


def dir_command(clientSocket):
    print("Execute command DIR") 				# debug print


def get_command(clientSocket, socketUDP, serverName, fname):
    print("Execute command GET file:", fname )	# debug print
    
    
    
def put_command(clientSocket, socketUDP, serverName, fname):
    print("Execute command PUT file:", fname )	# debug print
    



def main(args):
    if (len(args) > 2):
        serverName = args[1]
        serverPort1 = int(args[2])
    else:
        print("Invalid arguments")
        sys.exit(1)

	# create TCP socket
    clientSocket = socket(AF_INET,SOCK_STREAM)
	# open TCP connection
    clientSocket.connect((serverName, serverPort1))
	
    # create UDP socket
    clientSocketUDP = socket(AF_INET,SOCK_DGRAM)
    #clientSocketUDP.bind((serverName, serverUDPPort)) #which one should I bind, server or client?
    
    while True:
        line = input("> ")
        cmdLine = line.split()
        cmd = cmdLine[0]
        cmd = cmd.upper()
        nargs = len(cmdLine)
        
        
        clientSocket.send(line.encode('utf-8'))
        
        
        if cmd == "DIR":
            if nargs != 1:
                print("Invalid arguments")
            else:
                dir_command(clientSocket)
                #clientSocket.send(cmd.encode())
                print("Files in curent directory: ")
                while True:
                    files_dir = clientSocket.recv(2048).decode()
                    if files_dir == 'end':
                        break
                    print(files_dir)
                
                
        elif cmd == "GET":
            if nargs != 2:
                print("Invalid arguments")
            else:
                filename = cmdLine[1]
                filename = str(filename)
                print(filename)
                get_command(clientSocket,clientSocketUDP,serverName,filename)
               # clientSocket.send(cmd.encode('utf-8'))
               # clientSocket.send(filename.encode('utf-8'))
                serverUDPPort = clientSocket.recv(CHUNK).decode()
                OK = clientSocket.recv(CHUNK).decode()
                serverUDPPort = int(serverUDPPort)
                if OK == "OK":
                    clientSocketUDP.sendto(msgSTART.encode(), (serverName, serverUDPPort))
                    with open(filename, 'w', encoding='utf-8') as newfile:
                        while True:
                            decoded_sc, address = clientSocketUDP.recvfrom(CHUNK)
                            decoded_sc = decoded_sc.decode('utf-8')
                            newfile.writelines(decoded_sc)
                            rcv_ack = clientSocket.recv(CHUNK).decode()
                            print(rcv_ack)
                            print(getsizeof(decoded_sc))
                            if getsizeof(decoded_sc) < 512:
                                break
                    newfile.close()
                    print("file transfer finished")
                    
                else:
                    print("no such file in server directory")
                    
                
                
          
        elif cmd == "PUT":
            if nargs != 2:
                print("Invalid arguments")
            else:
                filename = cmdLine[1]
                put_command(clientSocket, clientSocketUDP, serverName, filename)
               # clientSocket.send(cmd.encode('utf-8'))
               # clientSocket.send(filename.encode('utf-8'))
                serverUDPPort = clientSocket.recv(2048).decode()
                if serverUDPPort == "error":
                    print("file with same name is in server dir")
                    break
                OK = clientSocket.recv(2048).decode()
                serverUDPPort = int(serverUDPPort)
                if OK == "OK":
                    clientSocketUDP.sendto(msgSTART.encode(), (serverName, serverUDPPort))
                if os.path.isfile(filename):
                    print("file found, file transfer started")
                    with open(filename, encoding = "utf-8") as f:
                       while True:
                           '''time.sleep() finctions to prevents mixing data, and data leaks '''
                           time.sleep(0.001)
                           contents = f.read(463) #463 chars + 49 bytes = 512 (CHUNK)
                           clientSocketUDP.sendto(contents.encode("utf-8"),(serverName, serverUDPPort))
                           time.sleep(0.001)
                           rcv_ack, address = clientSocketUDP.recvfrom(CHUNK)
                           print(rcv_ack)
                           if len(contents) < 463:
                               print('file transfer finished')
                               break
                               
                    f.close()
                else:
                    print("no such file in server directory")
                    
                    
        elif cmd == "QUIT":
            clientSocket.send(msgQUIT.encode())
            clientSocketUDP.close()
            clientSocket.close()
            print("Client shutting down")
            return 0
            break

        else:
            print("Command not found")
  
		# ...
    
    

if __name__ == '__main__':
    import pathlib
    import sys
    from socket import *
    from sys import getsizeof
    import os
    import time
    import os.path
    sys.exit(main(sys.argv))
    