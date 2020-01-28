import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect the socket to the port where the server is listening to
server_address = ('localhost', 10000)
print('client is now connecting to the port {server}' .format(server = server_address))
sock.connect(server_address)
try:
    # random modle to ask put and get request from the server.. the client can know whether the server has it locally or not ... it can tell the server client 3 has it
    # Send data
    message = 'This is data send from client side.'
    print('Sending the data """ {data}'.format(data=message))
    sock.sendall(message.encode())

    # here we receive message back from the server which tells us whether the operation was done successfully or not then we calculate the performance
    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print('Reciving the data from server ::: {data} '.format(data=data))

finally:
    print('closing socket in client side')
    sock.close()
