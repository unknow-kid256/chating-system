import socket
import select
import sys

# Define server address and port
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 12345

# Set up the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

def send_message(socket, message):
    socket.send(message.encode())

while True:
    sockets_list = [sys.stdin, client_socket]

    read_sockets, _, _ = select.select(sockets_list, [], [])

    for notified_socket in read_sockets:
        if notified_socket == client_socket:
            message = client_socket.recv(1024).decode()
            if not message:
                print("Connection closed by the server")
                sys.exit()
            else:
                print(f"Server: {message}")
        else:
            message = sys.stdin.readline()
            send_message(client_socket, message.strip())
