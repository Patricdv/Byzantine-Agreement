import socket
import thread
import sys
import os
import time
import uuid
from math import radians, cos, sin, asin, sqrt

HOST = ''
PORT = 50002

server1Host = '127.0.0.1'
server1Port = 50001
server3Host = '127.0.0.1'
server3Port = 50003
server4Host = '127.0.0.1'
server4Port = 50004

server1Value = 0
server2Value = 2
server3Value = 0
server4Value = 0

def connect(connection):
    # Connect with the client and generate a unique filename
    # fileName = "received-files/" + str(uuid.uuid4())

    try:
        # Save the coordinates file on the server directory
        message = connection.send(server2Value)

    except Exception as msg:
        connection.send("ERROR")
        #File Error.
        print("Error message: " + str(msg))
        return

def conectado(connection, client):
    ###Function that starts a new thread for the connection
    msg = connection.recv(1024)
    if (msg == "GETNUMBER"):
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
server3Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server4Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	server1Socket.connect((server1Host, int(server1Port)))
	print("Connected to 1!")

	server3Socket.connect((server3Host, int(server3Port)))
	print("Connected to 3!")

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
        thread.start_new_thread(conectado, tuple([connection, client]))

except KeyboardInterrupt:
    print("\n\n--- TCP connection ended ---")
    tcp.close()
    sys.exit()
