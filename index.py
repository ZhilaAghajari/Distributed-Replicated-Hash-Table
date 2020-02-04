# server side
import socket
import sys
import threading

# initializing hash-table to serve the request send to this current node ..
number_keys = 5000
thread_numbers = 3
hash_table = [[] for i in range(int(number_keys/thread_numbers))]

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
            return v
    print('this key has not yet set in my machine')
    locks[hash_key].release()
    return None # if the key is not there ? I don't think we need it, right?


# remember to count number of success and fails ..
def local_hashing(message):
    #message format -->  message =  request+' '+str(key)+' '+str(value)
    hostname = socket.gethostname();
    IPAddr = socket.gethostbyname(hostname)
    #external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')#get my public id

    print('yeahhh a request from my hashing table. IP: '+IPAddr)
    global hash_table
    # split the component of the new message ...
    temp = message.split(message)
    if(temp[0] == 'put'):
        insert(temp[1], temp[2]) # insert(key, value)
    elif(temp[0] == 'get'):
        search(temp[1]) # search(key)
    return True


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
        else:
            res = "Success"
        connection.sendall(str(res).encode())
        print(res)
    finally:
        connection.close()
