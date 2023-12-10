import tkinter as tk
import socket
import threading
import json
from tkinter import DISABLED, END, NORMAL, VERTICAL


# Define Window
root = tk.Tk()
root.title("Chat Server")
root.iconbitmap("icon.ico")
root.geometry("800x800")
root.resizable(0, 0)

# Define fonts and colors
my_font = ('SimSun', 14)
black = "#010101"
light_green = "#1fc742"
root.config(bg=black)

# Create a connection class to handle all the connection logic


class Connection:
    '''A class to store a connection and its information'''

    def __init__(self):
        self.host_ip = socket.gethostbyname(socket.gethostname())
        self.encoder = "utf-8"
        self.bytesize = 1024

        self.client_sockets = []
        self.client_ips = []
        self.banned_ips = []


# Define functions

def start_server(connection):
    '''Starts the server and listens for connections'''
    # Get the port number from the entry box and attache it to the connection object
    connection.port = int(port_entry.get())

    # Create a server socket
    connection.server_socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    connection.server_socket.bind((connection.host_ip, connection.port))
    connection.server_socket.listen()

    # Update the GUI
    start_button.config(state=DISABLED)
    end_button.config(state=NORMAL)
    port_entry.config(state=DISABLED)
    input_entry.config(state=NORMAL)
    send_button.config(state=NORMAL)
    message_button.config(state=NORMAL)
    kick_button.config(state=NORMAL)
    ban_button.config(state=NORMAL)
    history_listbox.delete(0, END)
    history_listbox.insert(0, f"Server started on port {connection.port}")

    # Create a thread to listen for connections
    connection_thread = threading.Thread(
        target=connect_client, args=(connection,))
    connection_thread.start()


def end_server(connection):
    '''Ends the server and closes all connections'''
    # Alert all clients that the server is closing
    message_packet = create_message(
        "DISCONNECT", "Admin (broadcast)", "Server is shutting down", light_green)
    message_json = json.dumps(message_packet)
    broadcast_message(connection, message_json.encode(connection.encoder))

    # Update the GUI
    start_button.config(state=NORMAL)
    end_button.config(state=DISABLED)
    port_entry.config(state=NORMAL)
    input_entry.config(state=DISABLED)
    send_button.config(state=DISABLED)
    message_button.config(state=DISABLED)
    kick_button.config(state=DISABLED)
    ban_button.config(state=DISABLED)
    history_listbox.insert(0, f"Server ended on port {connection.port}")

    # Close Server Socket
    connection.server_socket.close()


def connect_client(connection):
    '''Connects a client to the server'''
    while True:
        try:
            client_socket, client_address = connection.server_socket.accept()
            # Check to see if the client is banned
            if client_address[0] in connection.banned_ips:
                message_packet = create_message("DISCONNECT", "Admin (private)", "You are banned from the server", light_green
                                                )
                message_json = json.dumps(message_packet)
                client_socket.send(message_json.encode(connection.encoder))
                client_socket.close()
            else:
                # Send a message to the client to receive info
                message_packet = create_message(
                    "INFO", "Admin (private)", "Please enter your name", light_green)
                message_json = json.dumps(message_packet)
                client_socket.send(message_json.encode(connection.encoder))

                # Wait for a confirmation message verifying the connection
                message_json = client_socket.recv(
                    connection.bytesize).decode(connection.encoder)
                process_message(connection, message_json,
                                client_socket, client_address)
        except:
            break


def create_message(flag, name, message, color):
    '''Creates a JSON message to be sent to the clients'''
    message_packet = {
        "flag": flag,
        "name": name,
        "message": message,
        "color": color
    }

    return message_packet


def process_message(connection, message_json, client_socket, client_address=(0, 0)):
    '''Update server information based on the message received'''
    # Load the message packet
    message_packet = json.loads(message_json)

    # Get the flag
    flag = message_packet["flag"]
    name = message_packet["name"]
    message = message_packet["message"]
    color = message_packet["color"]

    if flag == "INFO":
        # Add the client to the client list
        connection.client_sockets.append(client_socket)
        connection.client_ips.append(client_address[0])

        # Broadcast the new connection to all clients and update the GUI
        message_packet = create_message(
            "MESSAGE", "Admin", f"{name} has joined the server", light_green)
        message_json = json.dumps(message_packet)
        broadcast_message(connection, message_json.encode(connection.encoder))

        # Update the GUI
        client_listbox.insert(
            END, f"Name: {name}    IP Address: {client_address[0]}")

        # Create a thread to listen for messages from the client
        client_thread = threading.Thread(
            target=receive_message, args=(connection, client_socket,))
        client_thread.start()

    elif flag == "MESSAGE":
        # Broadcast the message to all clients and update the GUI
        broadcast_message(connection, message_json)

        # Update the GUI
        history_listbox.insert(0, f"{name}: {message}")
        history_listbox.itemconfig(0, fg=color)

    elif flag == "DISCONNECT":
        # Close/disconnect the client socket
        index = connection.client_sockets.index(client_socket)
        connection.client_sockets.remove(client_socket)
        connection.client_ips.pop(index)
        client_listbox.delete(index)
        client_socket.close()

        # Broadcast the disconnection to all clients and update the GUI
        message_packet = create_message(
            "MESSAGE", "Admin  (broadcast)", f"{name} has left the server", light_green)
        message_json = json.dumps(message_packet)
        broadcast_message(connection, message_json.encode(connection.encoder))

        # Update the GUI
        history_listbox.insert(
            0, f"Admin (broadcast): {name} has left the server")

    else:
        # Catch errors
        history_listbox(0, "ERROR: Unrecognized message flag " + flag)


def broadcast_message(connection, message_json):
    '''Broadcasts a message to all clients. All JSON are encoded'''
    for client_socket in connection.client_sockets:
        client_socket.send(message_json)


def receive_message(connection, client_socket):
    '''Receives a message from a client'''
    while True:
        # Get the message from the client
        try:
            message_json = client_socket.recv(
                connection.bytesize)
            process_message(connection, message_json, client_socket)
        except:
            # Catch errors
            history_listbox.insert(
                END, "ERROR: Unable to receive message from client")
            break


def self_broadcast(connection):
    '''Broadcasts a special admin message to all clients'''
    # Create a message packet
    message_packet = create_message(
        "MESSAGE", "Admin (broadcast)", input_entry.get(), light_green)
    message_json = json.dumps(message_packet)
    broadcast_message(connection, message_json.encode(connection.encoder))

    # Clear the input entry
    input_entry.delete(0, END)


def private_message(connection):
    '''Sends a private message to a specific client'''
    # Select the client from the client listbox and access the client socket
    client_index = client_listbox.curselection()[0]
    client_socket = connection.client_sockets[client_index]

    # Create a message packet
    message_packet = create_message("MESSAGE", "Admin (private)",
                                    input_entry.get(), light_green)
    message_json = json.dumps(message_packet)
    client_socket.send(message_json.encode(connection.encoder))

    # Clear the input entry
    input_entry.delete(0, END)


def kick_client(connection):
    '''Kicks a client from the server'''
    # Select the client from the client listbox and access the client socket
    client_index = client_listbox.curselection()[0]
    client_socket = connection.client_sockets[client_index]

    # Create a message packet
    message_packet = create_message(
        "DISCONNECT", "Admin (private)", "You have been kicked from the server", light_green)
    message_json = json.dumps(message_packet)
    client_socket.send(message_json.encode(connection.encoder))


def ban_client(connection):
    '''Bans a client from the server'''
    # Select the client from the client listbox and access the client socket
    client_index = client_listbox.curselection()[0]
    client_socket = connection.client_sockets[client_index]
    client_ip = connection.client_ips[client_index]

    # Create a message packet
    message_packet = create_message(
        "DISCONNECT", "Admin (private)", "You have been banned from the server", light_green)
    message_json = json.dumps(message_packet)
    client_socket.send(message_json.encode(connection.encoder))

    # Ban the client
    connection.banned_ips.append(connection.client_ips[client_index])


# Define GUI Layout
# Create frames
connection_frame = tk.Frame(root, bg=black)
history_frame = tk.Frame(root, bg=black)
client_frame = tk.Frame(root, bg=black)
message_frame = tk.Frame(root, bg=black)
admin_frame = tk.Frame(root, bg=black)

connection_frame.pack(pady=5)
history_frame.pack()
client_frame.pack(pady=5)
message_frame.pack()
admin_frame.pack()

# Layout for the connection frame
port_label = tk.Label(connection_frame, text="Port Number:",
                      bg=black, fg=light_green, font=my_font)
port_entry = tk.Entry(connection_frame, bg=black,
                      fg=light_green, font=my_font, borderwidth=3, width=10)
start_button = tk.Button(connection_frame, text="Start Server",
                         font=my_font, bg=light_green, fg=black, borderwidth=5, command=lambda: start_server(my_connection))
end_button = tk.Button(connection_frame, text="End Server", font=my_font,
                       bg=light_green, fg=black, borderwidth=5, state=DISABLED, command=lambda: end_server(my_connection))

port_label.grid(row=0, column=0, padx=2, pady=10)
port_entry.grid(row=0, column=1, padx=2, pady=10)
start_button.grid(row=0, column=2, padx=2, pady=10)
end_button.grid(row=0, column=3, padx=2, pady=10)

# Layout for the history frame
hystory_scrollbar = tk.Scrollbar(
    history_frame, orient=VERTICAL)
history_listbox = tk.Listbox(history_frame, height=15, width=55, borderwidth=3,
                             bg=black, fg=light_green, font=my_font, yscrollcommand=hystory_scrollbar.set)
hystory_scrollbar.config(command=history_listbox.yview)

history_listbox.grid(row=0, column=0)
hystory_scrollbar.grid(row=0, column=1, sticky="NS")

# Layout for the client frame

client_scrollbar = tk.Scrollbar(client_frame, orient=VERTICAL)
client_listbox = tk.Listbox(client_frame, height=15, width=55, borderwidth=3,
                            bg=black, fg=light_green, font=my_font, yscrollcommand=client_scrollbar.set)
client_scrollbar.config(command=client_listbox.yview)

client_listbox.grid(row=0, column=0)
client_scrollbar.grid(row=0, column=1, sticky="NS")

# Layout for the message frame
input_entry = tk.Entry(message_frame, width=45, borderwidth=3,
                       font=my_font)
send_button = tk.Button(message_frame, text="Broadcast", borderwidth=5, width=10,
                        font=my_font, bg=light_green, state=DISABLED, command=lambda: self_broadcast(my_connection))
input_entry.grid(row=0, column=0, padx=5, pady=5)
send_button.grid(row=0, column=1, padx=5, pady=5)

# Layout for the admin frame

message_button = tk.Button(admin_frame, text="Send PM", font=my_font,
                           bg=light_green, fg=black, borderwidth=5, state=DISABLED, command=lambda: private_message(my_connection))
kick_button = tk.Button(admin_frame, text="Kick", font=my_font,
                        bg=light_green, fg=black, borderwidth=5, state=DISABLED, command=lambda: kick_client(my_connection))
ban_button = tk.Button(admin_frame, text="Ban", font=my_font,
                       bg=light_green, fg=black, borderwidth=5, state=DISABLED, command=lambda: ban_client(my_connection))

message_button.grid(row=0, column=0, padx=5, pady=5)
kick_button.grid(row=0, column=1, padx=5, pady=5)
ban_button.grid(row=0, column=2, padx=5, pady=5)

# Run root window's main loop

my_connection = Connection()
root.mainloop()
