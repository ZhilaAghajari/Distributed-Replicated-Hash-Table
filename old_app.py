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

def insert(key, value):
    global hash_table
    hash_key = hash(key)%len(hash_table)
    key_exists = False
    item = hash_table[hash_key]
    for i, kv in enumerate(item):
        k, v = kv # ?
        if key == k:
            key_exists = True
            #return False # key already exist, in this case we should return false , right?
            break
    if key_exists:
        item[i] =((key, value)) # in this case, only update the value of the corresponding key ?
        print('this pair already exists in the hash-table')
        return False #key already exist, in this case we should return false , or should we return item[i]?
    else:
        item.append((key, value)) #? does it change global hash table?
        print(' after insterting the hash-table is:')
        print(hash_table)
        return True

def get(key):
    global hash_table
    hash_key = hash(key)%len(hash_table)
    item = hash_table[hash_key]
    for i, kv in enumerate(item):
        k, v = kv
        if key==k:
            return v
    print('this key has not yet set in my machine')
    return False # if the key is not there ? I don't think we need it, right?


# remember to count number of success and fails ..
def local_hashing(message):
    #message format -->  message =  request+' '+str(key)+' '+str(value)
    hostname = socket.gethostname();
    IPAddr = socket.gethostbyname(hostname);
    print('yeahhh a request from my hashing table. IP: '+IPAddr)
    global hash_table
    # split the component of the new message ...
    temp = message.split(message)
    if(temp[0] == 'put'):
        insert(temp[1], temp[2]) # insert(key, value)
    elif(temp[0] == 'get'):
        search(temp[1]) # search(key)
    return True;


# Initialize the variables ..
# Update this part by reading this information from the property file
number_keys = 5000 # these keys are stored equally between nodes ( to know where they are stored, we can have
thread_numbers = 3
node_id = randint(1,number_keys) % thread_numbers
value = randint(1,999999)
key = randint(1,number_keys)
# create the hash table of the current node, based on the starting key it reads from the property file ..
# this hash table is global for the current client side ..
hash_table = [[] for i in range(int(number_keys/thread_numbers))]
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


