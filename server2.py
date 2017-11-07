import socket
import thread
import sys
import os
import time

HOST = ''
PORT = 50002

server1Host = '127.0.0.1'
server1Port = 50001
server3Host = '127.0.0.1'
server3Port = 50003
server4Host = '127.0.0.1'
server4Port = 50004

serverValue = 2
server1Values = [0, 0, 0, 0]
server2Values = [0, 2, 0, 0]
server3Values = [0, 0, 0, 0]
server4Values = [0, 0, 0, 0]


def getNumber(connection):
    try:
        connection.send("SENDNUMBER");
        serverNumber = connection.recv(8)
        print("getting information from server" + serverNumber)
        serverNumber = int(serverNumber)

        print '\nValue:',

        information = connection.recv(8)
        information = int(information)
        print information

        server2Values[serverNumber-1] = information

        if serverNumber == 1:
            time.sleep(5)

            server1Socket.send("GETNUMBER")
            returnMessage = server1Socket.recv(1024)
            if (returnMessage == "SENDNUMBER"):
                print("Connection started with 1")
                sendNumber(server1Socket)

            server3Socket.send("GETNUMBER")
            returnMessage = server3Socket.recv(1024)
            if (returnMessage == "SENDNUMBER"):
                print("Connection started with 3")
                sendNumber(server3Socket)

            server4Socket.send("GETNUMBER")
            returnMessage = server4Socket.recv(1024)
            if (returnMessage == "SENDNUMBER"):
                print("Connection started with 4")
                sendNumber(server4Socket)

            time.sleep(30)
            msg = connection.recv(1024)
            if (msg == "SENDSERVERVALUES"):
                print("Connection started to send server values")
                sendServerValues(connection)

        if serverNumber == 4:
            time.sleep(5)
            print server2Values

    except Exception as msg:
        connection.send("ERROR")
        #File Error.
        print("Error message: " + str(msg))
        return

def sendServerValues(connection):
    try:
        connection.send("GETVALUES");
        print "Sending Server Values"
        connection.send(str(serverValue))

        connection.send(str(server2Values[0]))
        connection.send(str(server2Values[1]))
        connection.send(str(server2Values[2]))
        connection.send(str(server2Values[3]))

        print "Finish Sending Values"

    except Exception as msg:
        connection.send("ERROR")
        #File Error.
        print("Error message: " + str(msg))
        return

def sendNumber(connection):
    print "Sending server number"
    connection.send(str(serverValue))
    time.sleep(1)
    print "Sending server value"
    connection.send(str(serverValue))

def connected(connection, client):
    ###  Function that starts a new thread for the connection
    msg = connection.recv(1024)
    if (msg == "GETNUMBER"):
        print("Connection started with " + str(client))
        getNumber(connection)
    elif (msg == "SENDSERVERVALUES"):
        print("Connection started to send server values")
        sendServerValues(connection)
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
        thread.start_new_thread(connected, tuple([connection, client]))

except KeyboardInterrupt:
    print("\n\n--- TCP connection ended ---")
    tcp.close()
    sys.exit()
