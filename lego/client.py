# Put this in lego and run

import socket
from const import *
from utils import parse_command

# target_host = "169.254.98.60" # Change this to the IP address of your server
# target_port = 27700 # Change this to the port of your server

# create a socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.settimeout(1)
# connect to the server
client.connect((host_ip, PORT))
# receive
response = client.recv(4096)
if response.decode() == "ready":
        print("Successful")
else:
        print("Not successful")
        exit()
        # send
# client.settimeout(0)
client.setblocking(True)
while 1:
        try:
                client.send("hello world".encode())
                server_msg = client.recv(4096).decode()
                print(server_msg)
                parse_command(server_msg)
                if server_msg == QUIT_MSG:
                        client.close()
                        break
        except OSError as e:
                if e.args[0] == 11:
                        # EAGAIN error
                        continue