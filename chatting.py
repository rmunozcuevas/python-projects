import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("www.python.org,", 80))

# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host, and a well-known port
serversocket.bind((socket.gethostname(), 80))
# become a server socket
serversocket.listen(5)

while True:
    (clientsocket, address) = serversocket.accept()

    ct = client_thread(clientsocket)
    ct.run()


