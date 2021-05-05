# Name: Chris Hauser
# Assignment: CS 372 Project 2
# Description: Client socket which connects to a server at a specific port and is able to send and receive
#  messages back and forth. Sends the total message length as the first portion of the stream.

from socket import *

# and https://realpython.com/python-sockets/#socket-api-overview Echo Client example.

host = 'localhost'
port = 5045
# Initialize a socket and connect to the host on port 5045
with socket(AF_INET, SOCK_STREAM) as clientSocket:
    clientSocket.connect((host ,port))
    print('Connected to: ' + host + ' on port: ' + str(port))
    print('Type /q to quit')

    # Build and encode the request, then send it off
    while True:
        msg = input("Enter a message to send:")
        if msg == '/q':
            clientSocket.send(msg.encode())
            break
        msg = str(len(msg)).encode() + bytes(3) + msg.encode()
        clientSocket.send(msg)
        # get the message from the server, decode it back to UTF-8, and print
        data = clientSocket.recv(40)
        data = data.split(bytes(3))
        dataLength = int(data[0].decode())
        totalMsg = data[1].decode()
        bytesReceived = len(totalMsg)
        # until the total length of the message as communicated by the server is received
        #  continue to receive chunks of data, adding them to the totalMsg buffer.
        while bytesReceived < dataLength:
            data = clientSocket.recv(40)
            totalMsg += data.decode()
            bytesReceived += len(data)
        print(totalMsg)
        # continuously print and flush the response buffer until the entire stream of data is received

print('Connection Closed')

