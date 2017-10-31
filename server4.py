import socket
import thread
import sys
import os
import time
import uuid
from math import radians, cos, sin, asin, sqrt

HOST = ''
PORT = 50004

server1Host = '127.0.0.1'
server1Port = 50001
server2Host = '127.0.0.1'
server2Port = 50002
server3Host = '127.0.0.1'
server3Port = 50003

server1Value = 0
server2Value = 0
server3Value = 0
server4Value = 4

def connect(connection):
    # Connect with the client and generate a unique filename
    fileName = "received-files/" + str(uuid.uuid4())

    try:
        # Save the coordinates file on the server directory
        file = open(fileName, 'wb')
        connection.send("READY")
        print("Downloading file...")

        while True:
            response = connection.recv(4096)
            if (response == "-END-"):
                file.close()
                break
            file.write(response)

        connection.send("FINISHED")
        print("Succesfully downloaded file as " + fileName)

        #########################################################
	    # Calculate the distance between the points and respond #
        #########################################################

        message = connection.recv(1024)
        if (message == "READY"):
            try:
                finalFile = open(fileName, 'rb')
                reading = finalFile.read(4096)
                connection.send(reading)
                while reading != "":
                    reading = finalFile.read(4096)
                    connection.send(reading)

                # waiting for finishing the file send
                time.sleep(1)
                connection.send("-END-")

                print("finished sending")
                finalFile.close()

                response = connection.recv(1024)

                # If the file has been sended successfully
                if (response == "FINISHED"):
                    print("File succesfully sended.")
                else:
                    print("Failed to send file.")

                connection.close()
            except Exception as msg:
                print("Error on send file:" + msg)
                connection.close()
        else:
            print("Error: Didn't expect the message: " + message)
            connection.close()

        #######################################################

    except Exception as msg:
        connection.send("ERROR")
        #File Error.
        print("Error message: " + str(msg))
        return

def conectado(connection, client):
    ###Function that starts a new thread for the connection
    msg = connection.recv(1024)
    if (msg == "GETFILE"):
        print("Connection started with " + str(client))
        connect(connection)
    else:
        connection.close()
    thread.exit()

# Create a socket that use IPV4 and TCP protocol
# Bind the port for this process conections
# Set the maximun number of queued connections
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
origin = (HOST, PORT)

try:
    tcp.bind(origin)
    print("Binded")
except socket.error as SBE:
    print("Bind failed!")
    print(SBE)
    sys.exit()

tcp.listen(5)

print("TCP started and already listening...")

# Server accept connections until a keyboard interrupt
# If there is a keyboard interrupt, release the port

time.sleep(30)

server1Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server2Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server3Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	server1Socket.connect((server1Host, int(server1Port)))
	print("Connected to 1!")

	server2Socket.connect((server2Host, int(server2Port)))
	print("Connected to 2!")

	server3Socket.connect((server3Host, int(server3Port)))
	print("Connected to 3!")

except socket.error as sem:
    print("ERROR: Couldn't connect.")
    print(sem)
    sys.exit()

# actualSocket.send("GETFILE")
# sendFile(host, port, filePath)

try:
    while True:
        connection, client = tcp.accept()

        # For every connect a new thread will be created
        thread.start_new_thread(conectado, tuple([connection, client]))

except KeyboardInterrupt:
    print("\n\n--- TCP connection ended ---")
    tcp.close()
    sys.exit()
