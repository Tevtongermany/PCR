import socket 
import sys
import time
import configparser
import os
import threading


settingsfilename = "serverconfig.ini"
if os.path.exists(settingsfilename): # check if config file
    config = configparser.ConfigParser()
    config.read(settingsfilename)
    port = config.get('Settings', 'port')
    hostname = config.get('Settings', 'IP')
    clientlimit = config.get('Settings', 'Client Limit')
else: # config file doesn't exit creating one
    config = configparser.ConfigParser()
    config['Settings'] = {'port': '8080','IP': '127.0.0.1','Client Limit': '16'}
    with open(settingsfilename, 'w') as f:
        config.write(f)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = hostname
port = int(port)
server_socket.bind((host, port))
server_socket.listen(int(clientlimit))
clients = []

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message)



def handle_client(client_socket,address):
    print(f"Connected with {str(address)}")
    clients.append(client_socket)
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                broadcast(message, client_socket)
        except:
            clients.remove(client_socket)
            print(f"Disconnected from {str(address)}")
            client_socket.close()
            return

def start_server():
    print(f"Server started on {host}:{port}")
    while True:
        client_socket, address = server_socket.accept()
        print(f"Client {address} connected")
        thread = threading.Thread(target=handle_client, args=(client_socket,address))
        thread.start()


start_server()