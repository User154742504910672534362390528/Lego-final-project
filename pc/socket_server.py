import socket
import threading
# from const import *
from ..lego.const import *
import time

# bind_ip = "169.254.98.60" # Replace this with your own IP address
# bind_port = 27700 # Feel free to change this port
# create and bind a new socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host_ip, PORT))
server.listen(5)
print("Server is listening on %s:%d" % (host_ip, PORT))

client, addr = server.accept()
print("Client connected " + str(addr))
client.send("ready".encode())
while True:
    # wait for client to connect
    try:
        
        # create and start a thread to handle the client
        # client_handler = threading.Thread(target = clientHandler, args=(client,))
        # client_handler.start()
        request = client.recv(1024)
        print("Received \"" + request.decode() + "\" from client")
        while 1:
            msg = input("Say something to the client: ")
            if msg == HELP_MSG:
                continue
            client.send(msg.encode())
            if msg == QUIT_MSG:
                # close the connection again
                # client_socket.close()
                # print("Connection closed")
                raise KeyboardInterrupt
    except KeyboardInterrupt:
        client.close()
        print("Connection closed")
        break