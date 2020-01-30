# client side
import socket
import sys
import random
from random import randint

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_server( message, server_ip):
    #connect the socket to the port where the server is listening to
    # server_address = ('localhost', 10000)
    server_address = (server_ip, 10000)
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
        amount_expected = len(message) # I will get true or false and then count the number of true as successful and False as unsuccessful

        while amount_received < amount_expected:
            print('amin')
            data = sock.recv(1024).decode('utf-8')
            print('zhila')
            # data = sock.recv()
            amount_received += len(data)
            print('Reciving the data from server ::: {data} '.format(data=data))


    finally:
        print('closing socket in client side')
        sock.close()
    return; # end of function connect_server

# Initialize the variables ..
# Update this part by reading this information from the property file
number_operations = 100 # do them in a for loop after doing for one operation
for i in range(number_operations):
    number_keys = 5000 # these keys are stored equally between nodes ( to know where they are stored, we can have
    thread_numbers = 3
    value = randint(1,999999)
    key = randint(1,number_keys)
    # create the hash table of the current node, based on the starting key it reads from the property file ..
    # this hash table is global for the current client side ..

    if (random.random() <0.4): # the operation type
        request = 'put'
        message =  request+' '+str(key)+' '+str(value)
    else:
        request = 'get'
        message =  request+' '+str(key)

    #calculate which node should serve this request :
    node_id = key%thread_numbers
    message = message+' '+str(node_id)
    # update ip address based on node_id calcualted above...
    server_ip = 'localhost'
    connect_server(message, server_ip)




