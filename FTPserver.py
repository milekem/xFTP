# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 20:43:39 2022

@author: milos
"""
import sys
import os
import os.path
import pathlib
from socket import *
from sys import getsizeof
import time

SSIZE = 2048
CHUNK = 512
msgQUIT = "QUIT"
msgDIR = "DIR"
msgGET = "GET"
msgPUT = "PUT"
msgACK = "ACK"
msgOK = "OK"
msgSTART = "START"

def main(args):
    if (len(args) > 2):
        serverPort = int(args[1])
        serverUDPPort = int(args[2])
    else:
        print("Invalid arguments")
        sys.exit(1)

    serverPort = int(args[1])
    serverUDPPort = int(args[2])
    serverSocket = socket(AF_INET,SOCK_STREAM)   # create TCP welcoming socket
    serverSocket.bind(("0.0.0.0", serverPort)) #bind socket
    serverSocketUDP = socket(AF_INET,SOCK_DGRAM) 
    serverSocketUDP.bind(("0.0.0.0", serverUDPPort))


    serverSocket.listen(1)  # begin listening for incoming TCP requests
    print("Server is running")
    
    connSocket, addr = serverSocket.accept()

    print("Connected by: ", str(addr))

    while True:     
    
    
    

        line = connSocket.recv(2048).decode()    # read a sentence of bytes
        print(line)
        
        command = line.split()
        recived_cmd = command[0].upper()
    
    
        if recived_cmd == msgDIR:
            # get the list of all files and directories
            dir_path = "."      # current path 
            dir_list = os.listdir(dir_path)
             
            print("Files and directories in '", dir_path, "' :")
            # list to store files
            res = []
            # print files only
            for path in os.listdir(dir_path):
                # check if current path is a file
                if os.path.isfile(os.path.join(dir_path, path)):
                    res.append(path)
            for f in res:
                print(f)
                connSocket.send(f.encode())
            time.sleep(0.01)
            connSocket.send('end'.encode())
            
            
    
        
        elif recived_cmd == msgGET:
            #decoded_fn = connSocket.recv(2048).decode()
            filename = command[1]
            print('Execute command GET')
            if os.path.isfile(filename):
                print("file found, file transfer started")
                connSocket.send(str(serverUDPPort).encode())
                connSocket.send(msgOK.encode())
                START, UDP_address = serverSocketUDP.recvfrom(CHUNK)
                with open(filename) as f:
                    while True:
                        ''' uncomment time.sleep() finctions to prevent mixing data, and data leaks '''
                        time.sleep(0.001)
                        contents = f.read(463) #463 chars + 49 bytes = 512 (CHUNK)
                        serverSocketUDP.sendto(contents.encode("utf-8"), UDP_address)
                        time.sleep(0.001)
                        connSocket.send(msgACK.encode())
                        if len(contents) < 463:
                            break
                    print('file transfer finished')
                    f.close()         
                            
            else:
                print("no such file in server directory")
                                
        elif recived_cmd == msgPUT:
            filename = command[1]
        #filename = connSocket.recvfrom(2048)
        #data, adress = file_name
        #decoded_fn = data.decode('utf-8')
            print('Execute command PUT')
            if os.path.isfile(filename):
                print("file already in directory")
                connSocket.send("error".encode())
            else:
                connSocket.send(str(serverUDPPort).encode())
                connSocket.send(msgOK.encode())
                START, UDP_address = serverSocketUDP.recvfrom(2048)
                print('file transfer began')
                with open(filename, 'w', encoding='utf-8') as newfile:
                    while True:
                        decoded_sc, address = serverSocketUDP.recvfrom(CHUNK)                
                        decoded_sc = decoded_sc.decode('utf-8')
                        newfile.write(decoded_sc)
                        serverSocketUDP.sendto(msgACK.encode("utf-8"), UDP_address)
                        if getsizeof(decoded_sc) < 512:
                            break
                    newfile.close()
                    print("file transfer finished")

        elif recived_cmd == "QUIT":
            serverSocket.listen(1)  # begin listening for incoming TCP requests
            print("Server is running")
            connSocket, addr = serverSocket.accept()
        
        else:
            print("Command not found")
  
		# ...# received from client'''
  

    connSocket.close()  # close TCP connection:
                        # the welcoming socket continues

if __name__ == '__main__':
    import pathlib
    import sys
    from socket import *
    from sys import getsizeof
    import os
    import time
    import os.path
    sys.exit(main(sys.argv))
