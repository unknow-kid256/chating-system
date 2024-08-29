import socket
import msvcrt
import time
import select

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER_PORT = 5555
SERVER_IP = "127.0.0.1"
client_socket.connect((SERVER_IP, SERVER_PORT))
client_socket.setblocking(False)
msg = ""
open_client_sockets = []
print("1 - is for sending a chat text only,(most contain the data, the len of the data)\r\n"
      "2 - is for manager only, its for manager to ordain who he want to,(most contain length of the nominee and the name)\r\n"
      "3 - is for manager only, manager can kick participants from chat,(most contain length of the person and the name)\r\n"
      "4 - is for manager only, manager can mute  participants in chat,(most contain length of the person and the name)\r\n"
      "5 - is for sending a private messages to other participate in chat(most contain,the name of the participate and lenght, the data and the len of the data)\r\n")
name = input("enter ur name to start chat with other!- ")
current_time = time.localtime()
formatted_time = time.strftime("%H:%M", current_time)
i = 0


def create_message(message_parse):
    command = message_parse[0]
    data = message_parse[1:len(message_parse)+1]
    return (f"{len(name)}{name}{command}{len(data)}{data}".strip()).encode()


while True:
    rlist, _, _ = select.select([client_socket], [], [], 0)
    if i == 0:
        client_socket.send(create_message("0this is my name"))
        i += 1
    if msvcrt.kbhit():
        key = msvcrt.getch()
        msg += key.decode()
        print(msg)
        if ord(key.decode()) == 13 or msg == 'quit':
            client_socket.send(create_message(msg))
            msg = ""
        if msg == 'quit':
            break

    for current_socket in rlist:
        message = client_socket.recv(1024).decode()
        index = 0
        num_str = ""
        while message[index].isnumeric():
            num_str += message[index]
            index += 1
        data_length = int(num_str)
        data = message[index+1:index + data_length + 1]
        print(data)
