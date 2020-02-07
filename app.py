# client side
import socket
import sys
import random
from random import randint
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_server( message, server_ip,sock):
    global num_success
    global num_unsuccessfull
    global nack
    global num_false
    #connect the socket to the port where the server is listening to
    server_address = (server_ip, 10000)
    #sock.connect(server_address)
    print('client is now connecting to the port {server}' .format(server = server_address))
    try:
        # random model to ask put and get request from the server.. the client can know whether the server has it locally or not ... it can tell the server client 3 has it
        # Send data
        #message = 'MessageFromApplication.'+' ' +  message
        print('Sending the data from application """ {data}'.format(data=message))
        try:
            sock.sendall(message.encode())
        except:
            sock =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(server_address)
            print('this is reconnection because of a broken pipeline')
            sock.sendall(message.encode())
            print('data has been sent after reconnection')
        # here we receive message back from the server which tells us whether the operation was done successfully or not then we calculate the performance
        #amount_expected = len(message) # I will get true or false and then count the number of true as successful and False as unsuccessful
        data = sock.recv(1024).decode('utf-8')
        print('Receiving the result from server ::: {data} '.format(data=data))
        if data == 'True':
            num_success = num_success+1
        if data == 'Nack':
            nack = nack + 1
            return 'Nack'
        if data == "None":
            num_unsuccessfull = num_unsuccessfull +1
            #print('The process was not done')

        if data== 'False':
            num_false = num_false +1


    finally:
        0
        #print('closing socket in client side')
        print('')
        #sock.close()
    return # end of function connect_server

# the main function goes here ...
# Initialize the variables ..
# Update this part by reading this information from the property file
number_operations = 10000 # do them in a for loop after doing for one operation
num_success=0
num_unsuccessfull=0
num_false =0
nack = 0
start_time = time.time()
#ips ...
#remove
# server_ip_mac_mini = '128.180.220.113' #university
# #server_ip_mac_mini = '192.168.1.8' #at home
# server_ip_mac_book = '128.180.204.171'
# #server_ip_mac_book = '192.168.1.5'
# server_ip_sunlab = '128.180.120.73'

#sunlab machines
server_ip_sunlab_eris = '128.180.120.73'
server_ip_sunlab_ariel = '128.180.120.65'
server_ip_sunlab_caliban ='128.180.120.66'
# sockets ..
sock = {}
sock['s1'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock['s2'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock['s3'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock['s1'].connect((server_ip_mac_mini,10000))
# sock['s2'].connect((server_ip_mac_book,10000))
# sock['s3'].connect((server_ip_mac_book,10000))
sock['s1'].connect((server_ip_sunlab_eris,10000))
sock['s2'].connect((server_ip_sunlab_ariel,10000))
sock['s3'].connect((server_ip_sunlab_caliban,10000))
for i in range(number_operations):
    number_keys = 300 # these keys are stored equally between nodes ( to know where they are stored, we can have
    node_numbers = 3 # change it to 3 after testing ..
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
    node_id = key%node_numbers
    message = message+' '+str(node_id)
    if node_id ==0:
        #corresponding_sock = socket['s1']
        #server_ip = server_ip_mac_mini
        server_ip = server_ip_sunlab_eris
        res_itr = connect_server(message, server_ip,sock['s1'])
        if res_itr == 'Nack':
            t = 1 #
            while(connect_server(message, server_ip, sock['s1']) =='Nack'):
                time.sleep(0.000001*t)
                #t = t*2
    elif node_id ==1:
        #corresponding_sock = socket['s2']
        #server_ip = server_ip_mac_book
        server_ip = server_ip_sunlab_ariel
        res_itr = connect_server(message, server_ip,sock['s2'])
        if res_itr == 'Nack':
            t = 1 #
            while(connect_server(message, server_ip, sock['s2']) =='Nack'):
                time.sleep(0.000001*t)
                #t = t*2
    elif node_id ==2:
        #server_ip = server_ip_sunlab
        server_ip = server_ip_sunlab_caliban
        res_itr = connect_server(message, server_ip, sock['s3'])
        if res_itr == 'Nack':
            t = 1 #
            while(connect_server(message, server_ip, sock['s3']) =='Nack'):
                time.sleep(0.000001*t)
                #t = t*2

    print('iteration: '+str(i))
    print(server_ip)

end_time = time.time()
time_period = end_time -start_time
print('percent of return true (put the new key-value pair):'+str(num_success/number_operations))
print('percent of return False (a value is associated with the key):'+str(num_false/number_operations))
print('percent of Un-success (return null in get):'+str(num_unsuccessfull/number_operations))

print('percent of un-acknowledged requests: '+str(nack/number_operations))

print('{opr} number of operations has been executed in {sec} seconds'.format(sec=time_period, opr=(number_operations)))
print('throughput is: {thro}'.format(thro=(number_operations/time_period)))



