import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SERVER_PORT = 5555
SERVER_IP = "127.0.0.1"
while True:
    message = input("what is ur name: ")
    client_socket.sendto(message.encode(),(SERVER_IP,SERVER_PORT))
    if message == "":
        break
