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
        # if data == 'True':
        #     num_success = num_success+1
        if data == 'Nack':
            nack = nack + 1
            return 'Nack'
        if data == "None":
            num_unsuccessfull = num_unsuccessfull +1
            #print('The process was not done')
        else :
            num_success = num_success +1
            print(data)
        # if data== 'False':
        #     num_unsuccessfull = num_unsuccessfull +1


    finally:
        0
        #print('closing socket in client side')
        print('')
        #sock.close()
    return # end of function connect_server

# the main function goes here ...
# Initialize the variables ..
# Update this part by reading this information from the property file
number_operations = 300 # do them in a for loop after doing for one operation
num_success=0
num_unsuccessfull=0
nack = 0
start_time = time.time()
#ips ...
server_ip_mac_mini = '128.180.220.113'
server_ip_mac_book = '128.180.204.171'
# sockets ..
sock = {}
sock['s1'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock['s2'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock['s1'].connect((server_ip_mac_mini,10000))
sock['s2'].connect((server_ip_mac_book,10000))
for i in range(number_operations):
    number_keys = 5000 # these keys are stored equally between nodes ( to know where they are stored, we can have
    thread_numbers = 2 # change it to 3 after testing ..
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
    if node_id ==0:
        #corresponding_sock = socket['s1']
        server_ip = server_ip_mac_mini
        res_itr = connect_server(message, server_ip,sock['s1'])
        if res_itr == 'Nack':
            t = 1 #
            while(connect_server(message, server_ip, sock['s1']) =='Nack'):
                time.sleep(0.000001*t)
                #t = t*2
    elif node_id ==1:
        #corresponding_sock = socket['s2']
        server_ip = server_ip_mac_book
        res_itr = connect_server(message, server_ip,sock['s2'])
        if res_itr == 'Nack':
            t = 1 #
            while(connect_server(message, server_ip, sock['s2']) =='Nack'):
                time.sleep(0.000001*t)
                #t = t*2
    print('iteration: '+str(i))
    print(server_ip)
    # server_ips = [server_ip_mac_mini, server_ip_mac ]
    # server_ip = server_ips[randint(0,1)]
    #server_ip = '128.180.204.171'
    # server_ip = 'localhost'

    # res_itr = connect_server(message, server_ip,corresponding_sock)
    # if res_itr == 'Nack':
    #     t = 1 #
    #     while(connect_server(message, server_ip, corresponding_sock) =='Nack'):
    #         time.sleep(0.000001*t)
    #         t = t*2


#sock.close()
end_time = time.time()
time_period = end_time -start_time
print('percent of success:'+str(num_success/number_operations))
print('percent of Unsuccess:'+str(num_unsuccessfull/number_operations))
print('percent of un-acknowledged requests: '+str(nack/number_operations))
print('{opr} number of operations has been executed in {sec} seconds'.format(sec=time_period, opr=(number_operations)))



