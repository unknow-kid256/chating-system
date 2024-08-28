import socket
import time
import select

# global variables
MAX_MSG_LENGTH = 1024
SERVER_PORT = 5555
SERVER_IP = "0.0.0.0"
MANAGERS_ARRAY = ["ariel", "shua"]
muted_socket_array = []


# splits the message to get the info
def parse_message(message_to_parse):
    # getting name
    index = 0
    num_str = ""
    while message_to_parse[index].isnumeric():
        num_str += message_to_parse[index]
        index += 1

    username_length = int(num_str)
    username = message_to_parse[index:index + username_length]
    index += username_length
    command = message_to_parse[index]
    index += 1
    if command == "5":
        num_str = ""
        while message_to_parse[index].isnumeric():
            num_str += message_to_parse[index]
            index += 1
        name_for_send_length = int(num_str)
        name_for_send = message_to_parse[index: index + name_for_send_length]
        num_str = ""
        while message_to_parse[index].isnumeric():
            num_str += message_to_parse[index]
            index += 1
        msg_to_send_length = int(num_str)
        msg_to_send = message_to_parse[index: index + msg_to_send_length]
        return username, command, msg_to_send, name_for_send
    num_str = ""
    while message_to_parse[index].isnumeric():
        num_str += message_to_parse[index]
        index += 1

    data_length = int(num_str)
    data = message_to_parse[index: index + data_length]
    return username, command, data, ""


# an action to kick members
def kick_action(selected_name):
    selected_socket = users[selected_name]['socket']
    open_client_sockets.remove(selected_socket)
    selected_socket.close()
    return f"{selected_name} has been kicked from the chat!"

def mute_action(selected_name):
    print(selected_name)
    selected_socket = users[selected_name]['socket']
    muted_socket_array.append(selected_socket)
    return "you cannot speak here"

def appointment_of_manager(selected_name):
    MANAGERS_ARRAY.append(selected_name)
    users[selected_name]['isAdmin'] = True
    return f"{selected_name} is now a manager"
# handling the request of the manager
def manager_handle_request(selected_name, action):
    if action == "2":
        manager_msg = appointment_of_manager(selected_name)
        return manager_msg
    if action == "3":
        kick_msg = kick_action(selected_name)
        return kick_msg
    if action == "4":
        mute_msg = mute_action(selected_name)
        return mute_msg

def send_message_handle(msg):
    return f"{len(msg)}:{msg}".encode()

# send only if someone left the chat
def left_chat_msg(socket_name):
    current_time = time.localtime()
    formatted_time = time.strftime("%H:%M", current_time)
    return f"{formatted_time} {socket_name}: has left the chat!"


# creating message to send for all member
def create_message(msg, socket_name):
    current_time = time.localtime()
    formatted_time = time.strftime("%H:%M", current_time)
    return f"{formatted_time} {socket_name}: {msg}"


# print client member to the server
def print_client_sockets(client_sockets):
    for c in client_sockets:
        print("\t", c.getpeername())


# open server for client
print("setting up server")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
print("server is running")

# using select method
open_client_sockets = []
messages_to_send = []
users = {}

i = 0
while True:
    rlist, wlist, _ = select.select([server_socket] + open_client_sockets, open_client_sockets, [])
    for current_socket in rlist:
        if current_socket is server_socket:
            connection, client_address = current_socket.accept()
            print("New client joined!", client_address)
            open_client_sockets.append(connection)
            print_client_sockets(open_client_sockets)
        else:
            data = current_socket.recv(MAX_MSG_LENGTH).decode()
            name, command, msg_data, name_for_send = parse_message(data)
            if "@" in name:
                current_socket.send(send_message_handle("u cannot use that name"))
            if not (current_socket in users.values()):
                admin = name in MANAGERS_ARRAY
                users = {
                    name: {
                        "socket": current_socket,
                        "isAdmin": admin  # or true
                    }
                }
                break
            if msg_data == "view-managers":
                array_as_string = ",".join(MANAGERS_ARRAY)
                current_socket.send(send_message_handle(array_as_string))
            if msg_data == "quit":
                for client_socket in open_client_sockets:
                    if client_socket is not current_socket and client_socket in wlist:
                        client_socket.send(send_message_handle(left_chat_msg(name)))
                open_client_sockets.remove(current_socket)
                current_socket.close()
                break
            else:
                messages_to_send.append((current_socket, msg_data, name, command, name_for_send))

    for message in messages_to_send:
        current_socket, data, name, command, name_for_send = message
        if not (current_socket in muted_socket_array):
            if command == "1":
                for client_socket in open_client_sockets:
                    if client_socket is not current_socket and client_socket in wlist:
                        client_socket.send(send_message_handle(create_message(data, name)))
                messages_to_send.remove(message)
            if command == "2" or command == "3" or command == "4":
                if users[name]['isAdmin']:
                    manager_handle_request(data, command)

                else:
                    text = ("you are not able to use the manager command,u are not a manager.\r\n"
                            "if u want to send a text use command 1, if its private use 5.")
                    current_socket.send(send_message_handle(text))
                messages_to_send.remove(message)
            elif command == 5:
                socket_to_send = users[name_for_send]['socket']
                socket_to_send.send(send_message_handle(data))
                messages_to_send.remove(message)
            elif command == 0:
                pass
        else:
            current_socket.send(send_message_handle("you here speak cannot"))
            messages_to_send.remove(message)