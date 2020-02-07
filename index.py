# server side
import socket
import sys
import threading
import math
import random
from random import randint
import urllib.request
import ssl
# Create the hash-table of this server ..
number_keys = 300
node_numbers = 3
hash_table = [[] for i in range(int(number_keys/node_numbers))]

locks = [threading.Lock() for _ in range(len(hash_table))]
# serve the recieved requests in this node:
def insert(key, value):
    global hash_table
    hash_key = hash(key)%len(hash_table)
    key_exists = False
    if(locks[hash_key].locked()):
        return 'Nack'
    locks[hash_key].acquire()
    item = hash_table[hash_key]
    for i, kv in enumerate(item):
        k, v = kv # ?
        if key == k:
            key_exists = True
            #return False # key already exist, in this case we should return false , right?
            break
    if key_exists:
        #item[i] =((key, value)) # in this case, only update the value of the corresponding key ? or don't do anything?
        print('this pair already exists in the hash-table')
        locks[hash_key].release()
        return False #key already exist, in this case we should return false , or should we return item[i]? zhila check
    else:
        item.append((key, value))
        # print(' after insterting the hash-table is:')
        # print(hash_table)
        locks[hash_key].release()
        return True

def get(key):
    global hash_table
    hash_key = hash(key)%len(hash_table)
    if(locks[hash_key].locked()):
        return 'Nack'
    locks[hash_key].acquire()
    item = hash_table[hash_key]
    for i, kv in enumerate(item):
        k, v = kv
        if key==k:
            #return True
            locks[hash_key].release()
            return v
    print('this key has not been set in my machine')
    locks[hash_key].release()
    return None # if the key is not there ? I don't think we need it, right?


# remember to count number of success and fails ..

# which node id I have : ...
#ips ...
server_ip_mac_mini = '128.180.220.113' #university
#server_ip_mac_mini = '192.168.1.8' #at home
server_ip_mac_book = '128.180.204.171'#university
#server_ip_mac_book = '192.168.1.5'
server_ip_sunlab_eris= '128.180.120.73' #sunlab
server_ip_sunlab_ariel = '128.180.120.65'
server_ip_sunlab_caliban ='128.180.120.66'
context = ssl._create_unverified_context()
#my_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')#get my public id
my_ip = urllib.request.urlopen('https://ident.me',context=context).read().decode('utf8')#get my public id

print('my ip')
print(my_ip)
#my_ip = '192.168.1.8' #home
# if my_ip == server_ip_mac_mini:
#     node_id = 0
# elif my_ip == server_ip_mac_book:
#     node_id = 1
# elif my_ip == server_ip_sunlab:
#     node_id = 2
if my_ip == server_ip_sunlab_eris:
    node_id = 0
elif my_ip == server_ip_sunlab_ariel:
    node_id = 1
elif my_ip == server_ip_sunlab_caliban:
    node_id = 2

#Initialize hash-table ( by the rate of 25% , 50%, 90% of its whole size .. )
start_key = node_id*(int(number_keys/node_numbers))
for i in range(math.floor(.90*(number_keys/node_numbers))):
    value = randint(1,999999)
    key = randint(start_key,start_key+math.floor(number_keys/node_numbers))
    res_init = insert(key,value)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IPAddr = socket.gethostbyname(socket.gethostname())
server_address = (str(IPAddr), 10000)
print('starting on {server_address} on port {port}' .format(server_address = sys.stderr,port = server_address))
sock.bind(server_address)

sock.listen(1) #put the socket in server mode
while True:

    print('waiting for a connection')
    connection, client_address = sock.accept() # waits for an incoming message ..
    print(connection, client_address)
    try:
        print('connection from {client}' .format(client=client_address))
        #while True:
        data=connection.recv(1024).decode('utf-8')
        print('Server is now receiving {data} '.format(data=str(data)))
        #data = data.split()
        temp = data.split()
        print(temp)
        print('TEMP IS ABOVE')
        request_type = temp[0]
        key = temp[1]
        value = temp[2]
        print('@@@')
        print(temp)
        #... split the comming message and then serve the service .... and send true or false to the application so that they can count how many percent of the messages were sreved successfully
        if request_type == 'put':
            res = insert(key, value)
        elif request_type =='get':
            res = get(key)
        #send the data back to the application who requested this request?
        print('sending result of the request back to the client side')
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        if res==None:
            res = "None"
        # else:
        #     res = "Success"
        connection.sendall(str(res).encode())
        print(res)
    finally:
        connection.close()
