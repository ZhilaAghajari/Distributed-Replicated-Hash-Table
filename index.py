# server side
import socket
import sys

# initializing hash-table to serve the request send to this current node ..
number_keys = 5000
thread_numbers = 3
hash_table = [[] for i in range(int(number_keys/thread_numbers))]

# serve the recieved requests in this node:
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
            data=connection.recv(1024).decode('utf-8')
            print('Server is now receiving {data} '.format(data=str(data)))
            #data = data.split()
            temp = data.split()
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
            print('@@@')
            connection.sendall(str(res).encode())
            # if data:
            #     print('sending data back to client: {data}'.format(data=data))
            #     #data=data[len(data)::-1] # reverse the string before sending it back
            #     connection.sendall(data)
            # else:
            #     print('no more data from {client} ..'.format(client = client_address))
            #     break
    finally:
        connection.close()
