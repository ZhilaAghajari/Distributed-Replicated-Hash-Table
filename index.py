# server side
import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
print('starting on {server_address} on port {port}' .format(server_address = sys.stderr,port = server_address))
sock.bind(server_address)

sock.listen(1) #put the socket in server mode

while True:
    print('waiting for a connection')
    connection, client_address = sock.accept() # waits for an incoming message
    print(connection, client_address)
    try:
        print('connection from {client}' .format(client=client_address))
        while True:
            data=connection.recv(16)
            # data = connection.recv()
            #data = data.split()
            print('Server is now recieving {data} '.format(data=data))
            if data:
                print('sending data back to client: {data}'.format(data=data))
                #data=data[len(data)::-1] # reverse the string before sending it back
                connection.sendall(data)
            else:
                print('no more data from {client} ..'.format(client = client_address))
                break
    finally:
        connection.close()

