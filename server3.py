import socket
import thread
import sys
import os
import time
import uuid
from math import radians, cos, sin, asin, sqrt

HOST = ''
PORT = 50003

server1Host = '127.0.0.1'
server1Port = 50001
server2Host = '127.0.0.1'
server2Port = 50002
server4Host = '127.0.0.1'
server4Port = 50004


serverValue = 1
server1Values = [0, 0, 0, 0]
server2Values = [0, 0, 0, 0]
server3Values = [0, 0, 3, 0]
server4Values = [0, 0, 0, 0]


def getNumber(connection):
    try:
        connection.send("SENDNUMBER");
        serverNumber = connection.recv(sizeof(int))
        serverNumber = int(serverNumber)
        print("getting information from server" + serverNumber)

        information = connection.recv(sizeof(int))
        print information

        server3Values[serverNumber-1] = int(information)

        if serverNumber == 2:
            time.sleep(5)
            server1Socket.send("GETNUMBER")
            server2Socket.send("GETNUMBER")
            server4Socket.send("GETNUMBER")

        if serverNumber == 4:
            time.sleep(5)
            print server3Values

    except Exception as msg:
        connection.send("ERROR")
        #File Error.
        print("Error message: " + str(msg))
        return

def sendNumber(connection):

    print "Sending server number"
    connection.send(str(serverValue))

    print "Sending server value"
    connection.send(str(serverValue))

def connected(connection, client):
    ###Function that starts a new thread for the connection
    msg = connection.recv(1024)
    if (msg == "GETNUMBER"):
        print("Connection started with " + str(client))
        getNumber(connection)
    elif (msg == "SENDNUMBER"):
        print("Connection started with " + str(client))
        sendNumber(connection)
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
server4Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	server1Socket.connect((server1Host, int(server1Port)))
	print("Connected to 1!")

	server2Socket.connect((server2Host, int(server2Port)))
	print("Connected to 2!")

	server4Socket.connect((server4Host, int(server4Port)))
	print("Connected to 4!")

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
        thread.start_new_thread(connected, tuple([connection, client]))

except KeyboardInterrupt:
    print("\n\n--- TCP connection ended ---")
    tcp.close()
    sys.exit()
