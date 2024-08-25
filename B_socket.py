import socket
import time

port = 8821
msg = ""
while True:
    while True:
        B_client = socket.socket()
        B_client.connect(("127.0.0.1", port))
        print("Side B connecting to port", port)
        msg = input("msg + port :")
        string = msg.split(":")
        port = int(string[-1])
        B_client.send(msg.encode())
        print("Side B disconnecting")
        B_client.close()
        break
    while True:
        B_socket = socket.socket()
        B_socket.bind(("127.0.0.1", port))
        B_socket.listen()
        print("Side A listening to port", port)
        (A_client, A_address) = B_socket.accept()
        data = A_client.recv(1024).decode()
        arr = data.split(":")
        print("Side A:", arr[0])
        port = int(arr[-1])
        A_client.close()
        B_socket.close()
        time.sleep(3)
        break
    if "exit" in msg:
        break
