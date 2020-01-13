# CSE3461 server side
from socket import *
import sys
import os

if len(sys.argv) != 2:
    print("Error: Two argumets expected")
    sys.exit()
try:
    port = int(sys.argv[1])
except ValueError:
    print("Wrong port number. \n")
    sys.exit()

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(("", port))
sock.listen(1)
buffer_size = 10000
print("Listing on port ", port)
while 1:
    conn, addr = sock.accept()
    print ("Client connected: ", addr)
    while 1:
        data = conn.recv(buffer_size)
        if data:
            data = data.decode()
            print ("Received command ", data)
            startFile = data.find('<')
            endFile = data.find('>')
            nameLength = endFile - startFile - 1
            if data[:4] == "READ":
                if startFile == -1 or endFile == -1 or nameLength == 0:
                    print ("Sending back: Missing element READ... ")
                    conn.sendall(("Missing element: " + data + "\n    READ <filename>").encode())
                elif not os.path.exists(data[6:endFile]):
                    print ("Sending back: File does not exist...")
                    conn.sendall(("File " + data[6:endFile] + " does not exist").encode())
                else:
                    f = open(data[6:endFile])
                    contents = f.read()
                    if len(contents) == 0:
                        print ("Sending back: The file is empty...")
                        conn.sendall("The file is empty".encode())
                    else:
                        print ("Sending back: (contents...)")
                        contents = contents.encode()
                        conn.sendall(contents)
            elif data[:5] == "WRITE":
                if startFile == -1 or endFile == -1 or nameLength == 0:
                    print ("Sending back: Missing element: WRITE...")
                    conn.sendall(("Missing element: " + data + "\n    WRITE <filename> string").encode())
                elif not os.path.exists(data[7:endFile]):
                    print ("Sending back: File does not exist...")
                    conn.sendall(("File " + data[7:endFile] + " does not exist").encode())
                else:
                    f = open(data[7:endFile], "w+")
                    f.write(data[endFile+2:])
                    f.close()
                    print ("Sending back: Sucessfully WRITE FILE... ")
                    conn.sendall(("Sucessfully WRITE FILE " + data[7:endFile]).encode())
            elif data[:4] == "LIST":
                dirs = os.listdir()
                print ("Sending back: ")
                for f in dirs:
                    print (f + " ")
                    conn.sendall((f + '\n').encode())
            elif data[:6] == "DELETE":
                if startFile == -1 or endFile == -1 or nameLength == 0:
                    print ("Sending back: Missing element: DELETE...")
                    conn.sendall("Missing element: DELETE\n    DELETE <filename>".encode())
                elif not os.path.exists(data[8:endFile]):
                    print ("Sending back: File does not exist...")
                    conn.sendall(("File " + data[8: endFile] + " does not exist").encode())
                else:
                    os.remove(data[8:endFile])
                    print ("Sending back: Successfully delete file... ")
                    conn.sendall(("Successfully delete file " + data[8: endFile]).encode())
            elif data[:6] == "CREATE":
                if startFile == -1 or endFile == -1 or nameLength == 0:
                    print ("Sending back: Missing element: CREATE...")
                    conn.sendall("Missing element: CREATE\n    CREATE <filename>".encode())
                else:
                    f = open(data[8:endFile], "w+")
                    f.close()
                    print ("Sending back: Created file " + data[8:endFile])
                    conn.sendall(("Created file " + data[8:endFile]).encode())
            else:
                print ("Sending back: Invalid command...")
                feedback = ("Invalid command: " + data + "\nCommands:\n    READ\n    WRITE\n    LIST\n    DELETE\n    CREATE").encode()
                conn.sendall(feedback)
	    
sock.close()





