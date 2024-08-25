import socket
import time

port = 8821
msg = ""
while True:
    while True:
        A_socket = socket.socket()
        A_socket.bind(("127.0.0.1", port))
        A_socket.listen()
        print("Side A listening to port", port)
        (B_client, B_address) = A_socket.accept()
        data = B_client.recv(1024).decode()
        arr = data.split(":")
        print("Side A:", arr[0])
        port = int(arr[-1])
        B_client.close()
        A_socket.close()
        time.sleep(3)
        break
    while True:
        A_client = socket.socket()
        A_client.connect(("127.0.0.1", port))
        print("Side B connecting to port", port)
        msg = input("msg + port:")
        string = msg.split(":")
        port = int(string[-1])
        A_client.send(msg.encode())
        print("Side B disconnecting")
        A_client.close()
        break
    if msg == "exit":
        break