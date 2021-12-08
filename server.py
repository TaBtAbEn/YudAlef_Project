import socket
import select
import pickle

MAX_MSG_LENGTH = 2048
SERVER_PORT = 5555
SERVER_IP = '127.0.0.1'
c = 0

def print_client_sockets(client_sockets):
    for c in client_sockets:
        print("\t", c.getpeername())

print("Setting up server...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
print("Listening for clients...")

client_sockets = []
messages_to_send = []
while True:
    rlist, wlist, xlist = select.select([server_socket] + client_sockets, client_sockets, [])
    # rlist, wlist, xlist = [server_socket] + client_sockets, [], []
    for current_socket in rlist:
        if current_socket is server_socket:
            connection, client_address = current_socket.accept()
            print("New client joined!", client_address)
            client_sockets.append(connection)
            print_client_sockets(client_sockets)
            c = int(c)
            c = c+1
            c = str(c)
            connection.send(c.encode())
            print("Number of people that enter the server: ",c)
        else:
            #if current_socket in wlist:
            data = pickle.loads(current_socket.recv(MAX_MSG_LENGTH))


            if data == [['e', 'e', 'e'], ['e', 'e', 'e'], ['e', 'e', 'e']]: # client disconnected!!!
                print("Connection closed with ",current_socket )
                client_sockets.remove(current_socket)
                current_socket.close()
                print_client_sockets(client_sockets)
            else: # client sent something
                print(current_socket, 'is playing: ', data)
                sendData=pickle.dumps(data)

                messages_to_send.append((current_socket, data))
                #((sock1, messahe_to_sock1), (sock2, message_to_sock2)...)

    for message_tuple in messages_to_send: #message_tuple = (sock_i, message_to_sock_i)
        current_socket, message = message_tuple
        for send_socket in client_sockets:
            if current_socket != send_socket:

                send_socket.send(sendData)
    messages_to_send = []
