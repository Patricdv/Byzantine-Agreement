import socket
import thread
import sys
import os
import time

HOST = ''
PORT = 50001

server2Host = '127.0.0.1'
server2Port = 50002
server3Host = '127.0.0.1'
server3Port = 50003
server4Host = '127.0.0.1'
server4Port = 50004

serverValue = 1
server1Values = [1, 0, 0, 0]
server2Values = [1, 2, 6, 4]
server3Values = [1, 2, 3, 4]
server4Values = [1, 2, 7, 4]

serversQuantity = 4
testServers = {}

def doByzantineAgreement():
    print "\nStarting Byzantine Agreement:"
    print "Server Values:"
    print server1Values
    print server2Values
    print server3Values
    print server4Values

    count = 0
    percentage = 100/serversQuantity
    for key in range(0, serversQuantity):
        print "testing server: ",
        print key

        testServers = {}
        count = 0
        testServers.update({server1Values[key]: percentage})

        if server2Values[key] in testServers:
            testServers[server2Values[key]] += percentage
        else:
            testServers.update({server2Values[key]: percentage})

        if server3Values[key] in testServers:
            testServers[server3Values[key]] += percentage
        else:
            testServers.update({server3Values[key]: percentage})

        if server4Values[key] in testServers:
            testServers[server4Values[key]] += percentage
        else:
            testServers.update({server4Values[key]: percentage})

        for x in testServers:
            if testServers[x] >= 60:
                count +=1
                print "Server ",
                print key+1,
                print " isn't a traitor"
                break

        if count == 0:
            print "This sith server ",
            print key+1,
            print " is a traitor"

def receiveServerValues(connection):
    serverNumber = connection.recv(8)
    serverNumber = int(serverNumber)

    serverValues = [0, 0, 0, 0]
    serverValues[0] = connection.recv(8)
    serverValues[1] = connection.recv(8)
    serverValues[2] = connection.recv(8)
    serverValues[3] = connection.recv(8)

    print serverNumber

    if serverNumber == 2:
        server2Values[0] = int(serverValues[0])
        server2Values[1] = int(serverValues[1])
        server2Values[2] = int(serverValues[2])
        server2Values[3] = int(serverValues[3])

    if serverNumber == 3:
        server3Values[0] = int(serverValues[0])
        server3Values[1] = int(serverValues[1])
        server3Values[2] = int(serverValues[2])
        server3Values[3] = int(serverValues[3])

    if serverNumber == 4:
        server4Values[0] = int(serverValues[0])
        server4Values[1] = int(serverValues[1])
        server4Values[2] = int(serverValues[2])
        server4Values[3] = int(serverValues[3])

def getAllValues():
    server2Socket.send("SENDSERVERVALUES")
    returnMessage = server2Socket.recv(1024)
    if (returnMessage == "GETVALUES"):
        print("Connection started with 2")
        receiveServerValues(server2Socket)

    server3Socket.send("SENDSERVERVALUES")
    returnMessage = server3Socket.recv(1024)
    if (returnMessage == "GETVALUES"):
        print("Connection started with 3")
        receiveServerValues(server3Socket)

    server4Socket.send("SENDSERVERVALUES")
    returnMessage = server4Socket.recv(1024)
    if (returnMessage == "GETVALUES"):
        print("Connection started with 4")
        receiveServerValues(server4Socket)

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

        server1Values[serverNumber-1] = information
        if serverNumber == 4:
            time.sleep(5)
            print server1Values

            time.sleep(60)
            getAllValues()

            doByzantineAgreement()

    except Exception as msg:
        connection.send("ERROR")
        #File Error.
        print("Error message: " + str(msg))
        return

def sendServerValues(connection):
    try:
        connection.send("GETVALUES");
        print "Sending Server Values"
        time.sleep(1)
        connection.send(str(serverValue))

        for value in server1Values:
            connection.send(str(value))

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
    ###Function that starts a new thread for the connection
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

server2Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server3Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server4Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	server2Socket.connect((server2Host, int(server2Port)))
	print("Connected to 2!")

	server3Socket.connect((server3Host, int(server3Port)))
	print("Connected to 3!")

	server4Socket.connect((server4Host, int(server4Port)))
	print("Connected to 4!")

except socket.error as sem:
    print("ERROR: Couldn't connect.")
    print(sem)
    sys.exit()

server2Socket.send("GETNUMBER")
returnMessage = server2Socket.recv(1024)
if (returnMessage == "SENDNUMBER"):
    print("Connection started with 2")
    sendNumber(server2Socket)

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

try:
    while True:
        connection, client = tcp.accept()

        # For every connect a new thread will be created
        thread.start_new_thread(connected, tuple([connection, client]))

except KeyboardInterrupt:
    print("\n\n--- TCP connection ended ---")
    tcp.close()
    sys.exit()
