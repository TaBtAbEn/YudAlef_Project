import socket
import select



MAX_MSG_LENGTH = 1024
SERVER_PORT = 5555
SERVER_IP = "127.0.0.1"
print("Setting up server...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
print("Listening for clients...")
client_sockets = []
all_clients = {}
while True:
    rlist, wlist, xlist = select.select([server_socket] + client_sockets, [], [])
    for current_socket in rlist:
        if current_socket is server_socket:
            connection, client_address = current_socket.accept()
            print("New client joined!", client_address)
            client_sockets.append(connection)
            connection.send("what do you want to do?".encode())
            print("sent to ", client_address, ": what do you want to do?")
        else:

            data = current_socket.recv(MAX_MSG_LENGTH).decode()
            if data == "set my name and password":
                #ליעל את הפעולה!
                print(client_address, "client want to set up his username and password")
                connection.send("Enter name".encode())
                name = current_socket.recv(MAX_MSG_LENGTH).decode()
                all_clients[name] = current_socket
                connection.send("Enter password".encode())
                password = current_socket.recv(MAX_MSG_LENGTH).decode()
                print(all_clients)

            if data == "close connection":
                print("Connection closed", client_address)
                client_sockets.remove(current_socket)
                current_socket.close()

"""
"ori": socket
"gilad: 
"""


def send_msg(name):
    recever=all_clients[name]
