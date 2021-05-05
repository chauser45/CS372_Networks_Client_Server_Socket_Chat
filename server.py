# Name: Chris Hauser
# Assignment: CS 372 Project 2
# Description: Server socket which connects to a server at a specific port and is able to send and receive
# messages back and forth. Sends the total message length as the first portion of the stream.

from socket import *

# Code adapted from https://realpython.com/python-sockets/#socket-api-overview
# Echo Server example.
host = 'localhost'
port = 5045
#  initialize a socket set up for TCP connection
with socket(AF_INET, SOCK_STREAM) as serverSocket:
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # create the socket on local host with the given arbitrary port.
    serverSocket.bind((host,port))
    # Allow the socket to receive requests and accept the first one that arrives
    serverSocket.listen()

    print('Server listening on:' + '(' + host + ',' + str(port) + ')')
    connection, address = serverSocket.accept()
    # print the details of the connecting client, receive their GET request and print it.
    with connection:

        print("Connected to:" + str(address))
        while True:

            data = connection.recv(40)
            # end the connection if quit message received
            if data.decode() == '/q':
                break
            # use the delimiter character of bytes(3) to split the incoming first message
            #  into its total length and the first data segment
            data = data.split(bytes(3))
            dataLength = int(data[0].decode())
            totalMsg = data[1].decode()
            bytesReceived = len(totalMsg)
            # until the total length of the message as communicated by the client is received
            #  continue to receive chunks of data, adding them to the totalMsg buffer.
            while bytesReceived < dataLength:
                data = connection.recv(40)
                totalMsg += data.decode()
                bytesReceived += len(data)
            print(totalMsg)
            msg = input("Enter a message to send:")
            msg = str(len(msg)).encode() + bytes(3) + msg.encode()
            connection.sendall(msg)
print('Connection closed')



