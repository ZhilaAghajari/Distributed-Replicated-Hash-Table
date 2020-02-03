# client side
import socket
import sys
import random
from random import randint

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_server( message, server_ip):
    global num_success
    global num_unsuccessfull
    #connect the socket to the port where the server is listening to
    # server_address = ('localhost', 10000)
    server_address = (server_ip, 10000)
    print('client is now connecting to the port {server}' .format(server = server_address))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    try:
        # random model to ask put and get request from the server.. the client can know whether the server has it locally or not ... it can tell the server client 3 has it
        # Send data
        #message = 'MessageFromApplication.'+' ' +  message
        print('Sending the data from application """ {data}'.format(data=message))
        sock.sendall(message.encode())

        # here we receive message back from the server which tells us whether the operation was done successfully or not then we calculate the performance
        #amount_expected = len(message) # I will get true or false and then count the number of true as successful and False as unsuccessful
        data = sock.recv(1024).decode('utf-8')
        print('Receiving the result from server ::: {data} '.format(data=data))
        if data == 'True':
            num_success = num_success+1
        if data == "None":
            print('The process was not done')
        if data== 'False':
            num_unsuccessfull = num_unsuccessfull +1


    finally:
        print('closing socket in client side')
        sock.close()
    return # end of function connect_server

# Initialize the variables ..
# Update this part by reading this information from the property file
number_operations = 300 # do them in a for loop after doing for one operation
num_success=0
num_unsuccessfull=0
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
    # if node_id == 0:
    #     server_ip = 'localhost'
    # elif node_id ==1:
    #     server_ip = ''
    # elseif node_id ==2:
    #     server_ip=''
    #server_ip = '192.168.1.8.'
    server_ip = 'localhost'
    print('iteration: '+str(i))
    print(message)
    connect_server(message, server_ip)

print('percent of success:'+str(num_success/number_operations))
print('percent of Unsuccess:'+str(num_unsuccessfull/number_operations))




