# client side
import socket
import sys
import random
from random import randint

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_server( message):
    #connect the socket to the port where the server is listening to
    server_address = ('localhost', 10000)
    print('client is now connecting to the port {server}' .format(server = server_address))
    sock.connect(server_address)
    try:
        # random model to ask put and get request from the server.. the client can know whether the server has it locally or not ... it can tell the server client 3 has it
        # Send data
        #message = 'MessageFromApplication.'+' ' +  message
        print('Sending the data """ {data}'.format(data=message))
        sock.sendall(message.encode())

        # here we receive message back from the server which tells us whether the operation was done successfully or not then we calculate the performance
        # Look for the response
        amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = sock.recv(16)
            # data = sock.recv()
            amount_received += len(data)
            print('Reciving the data from server ::: {data} '.format(data=data))

    finally:
        print('closing socket in client side')
        sock.close()
    return; # end of function connect_server


def local_hashing(message):
    #message format -->  message =  request+' '+str(key)+' '+str(value)
    hostname = socket.gethostname();
    IPAddr = socket.gethostbyname(hostname);
    print('yeahhh a request from my hashing table. IP: '+IPAddr)

    return True;


#the program flow ..
# update this part by reading this information from the property file
number_keys = 5000 # these keys are stored equally between nodes ( to know where they are stored, we can have
thread_numbers = 3
node_id = randint(1,number_keys) % thread_numbers
value = randint(1,999999)
key = randint(1,number_keys)
# create the hash table of the current node, based on the starting key it reads from the property file ..

number_operations = 100000 # do them in a for loop after doing for one operation
if (random.random() <0.4): # the operation type
    request = 'put'
    message =  request+' '+str(key)+' '+str(value)
else:
    request = 'get'
    message =  request+' '+str(key)

if node_id == 0:
    local_hashing(message)
else:
    #connect the server to call the corresponding server ..
    message = message + ' ' + str(node_id)
    connect_server(message)
# to seperate the elements of the received message do the following
#message.split()


