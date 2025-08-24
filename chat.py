import socket

stream_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM)

host = "localhost"

port="8080"

server_address = ((host, port))

print("connecting")

stream_socket.connect(server_address)

message = 'message'
stream_socket.sendall(message.encode())

data = stream_socket.recv(10)
print(data)

print('socket closed')

## FULL CODE FOR CLIENT/SERVER UP 


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((host, port))

sock.listen(1)

print('waiting for a connection')
connection, client = sock.accept()

print(client, 'connected')

data = connection.recv(16)
print('received "%s"' % data)
if data:
    connection.sendall(data)
else:
    print('no data from', client)

connection.close()


