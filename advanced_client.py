
# Client Side GUI for the chat application
import tkinter
import socket
import threading
from tkinter import DISABLED, VERTICAL, END, NORMAL, StringVar
import json

# Define Window
root = tkinter.Tk()
root.title("Chat Application")
root.iconbitmap("icon.ico")
root.geometry("700x750")
root.resizable(0, 0)


# Define Fonts and Colors

my_font = ("Arial", 14)
greay_grey = "#2f2f2f"
light_green = "#7ed957"
white = "#ffffff"
orange = "#ff862f"
pink = "#ff0080"
blue = "#00bfff"
yellow = "#ffff00"
purple = "#800080"
root.config(bg=greay_grey)


class Connection():
    '''A class to store a connectiopn  - a client socket and its information'''

    def __init__(self):
        self.encoder = "utf-8"
        self.bytesize = 1024

# Define Functions


def connect(connection):
    '''Connect to a server at a given ip/port address'''
    # Clear any previous chats
    my_listbox.delete(0, END)

    # Get the required information from the GUI
    connection.name = name_entry.get()
    connection.host_ip = ip_entry.get()
    connection.port = int(port_entry.get())
    connection.color = color.get()

    try:
        # Create a client socket
        connection.client_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        connection.client_socket.connect((connection.host_ip, connection.port))

        # Receive the server's welcome message
        message_json = connection.client_socket.recv(
            connection.bytesize).decode(connection.encoder)
        process_message(connection, message_json)
    except:
        my_listbox.insert(END, "Error connecting to server")
        return


def disconnect(connection):
    ''' Disconnects from the server. '''
    # Create message packet
    message_packet = create_message(
        "DISCONNECT", connection.name, "Left the chat", connection.color)
    message_json = json.dumps(message_packet)
    connection.client_socket.send(message_json.encode(connection.encoder))

    # Disable the GUI for chatting
    gui_end()


def gui_start():
    '''Starts the GUI for the chat application'''
    connect_button.config(state=DISABLED)
    disconnect_button.config(state=NORMAL)
    name_entry.config(state=DISABLED)
    ip_entry.config(state=DISABLED)
    port_entry.config(state=DISABLED)
    for button in color_buttons:
        button.config(state=DISABLED)
    input_entry.config(state=NORMAL)
    send_button.config(state=NORMAL)


def gui_end():
    '''Ends the GUI for the chat application'''
    connect_button.config(state=NORMAL)
    disconnect_button.config(state=DISABLED)
    name_entry.config(state=NORMAL)
    ip_entry.config(state=NORMAL)
    port_entry.config(state=NORMAL)
    for button in color_buttons:
        button.config(state=NORMAL)
    input_entry.config(state=DISABLED)
    send_button.config(state=DISABLED)


def create_message(flag, name, message, color):
    '''Creates a JSON message to be sent to the clients'''
    message_packet = {
        "flag": flag,
        "name": name,
        "message": message,
        "color": color
    }

    return message_packet


def process_message(connection, message_json):
    '''Update client based on message packet flag'''
    # Update the chat history by unpacking the message packet
    message_packet = json.loads(message_json)
    flag = message_packet["flag"]
    name = message_packet["name"]
    message = message_packet["message"]
    color = message_packet["color"]

    if flag == "INFO":
        # Server asking ionformation about the client. Send the name and color
        message_packet = create_message(
            "INFO", connection.name, "Joined the chat", connection.color)
        message_json = json.dumps(message_packet)
        connection.client_socket.send(message_json.encode(connection.encoder))

        # Enable the GUI for chatting
        gui_start()

        # Create a thread to constantly receive messages from the server
        receive_thread = threading.Thread(
            target=receive_message, args=(connection,))
        receive_thread.start()
    elif flag == "MESSAGE":
        # Server sending a message to the client
        my_listbox.insert(0, f"{name}: {message}")
        my_listbox.itemconfig(0, fg=color)

    elif flag == "DISCONNECT":
        # Server sending a disconnect message to the client
        my_listbox.insert(0, f"{name}: {message}")
        my_listbox.itemconfig(0, fg=color)
        disconnect(connection)

    else:
        # Catch for errors
        my_listbox.insert(END, "Error receiving message from server")


def send_message(connection):
    '''Sends a message to the server'''
    # Send the message to the server
    message_packet = create_message("MESSAGE", connection.name,
                                    input_entry.get(), connection.color)
    message_json = json.dumps(message_packet)
    connection.client_socket.send(message_json.encode(connection.encoder))

    # Clear the input field
    input_entry.delete(0, END)


def receive_message(connection):
    '''Receives a message from the server'''
    while True:
        # Receive incoming message from server
        try:
            # Receve an incoming message packet
            message_json = connection.client_socket.recv(
                connection.bytesize).decode(connection.encoder)
            process_message(connection, message_json)
        except:
            # Catch errors
            my_listbox.insert(0, "Connection has been closed by the server")

            break


# Define GUI Layout
# Create Frames
info_frame = tkinter.Frame(root, bg=greay_grey)
color_frame = tkinter.Frame(root, bg=greay_grey)
output_frame = tkinter.Frame(root, bg=greay_grey)
input_frame = tkinter.Frame(root, bg=greay_grey)

info_frame.pack()
color_frame.pack()
output_frame.pack(pady=10)
input_frame.pack()

# Info Frame Layout

name_label = tkinter.Label(info_frame, text="Name:",
                           bg=greay_grey, fg=light_green, font=my_font)
name_entry = tkinter.Entry(
    info_frame, bg=greay_grey, fg=light_green, font=my_font, borderwidth=3)
ip_label = tkinter.Label(info_frame, text="Host IP:",
                         bg=greay_grey, fg=light_green, font=my_font)
ip_entry = tkinter.Entry(info_frame, bg=greay_grey,
                         fg=light_green, font=my_font, borderwidth=3)
port_label = tkinter.Label(info_frame, text="Port:",
                           bg=greay_grey, fg=light_green, font=my_font)
port_entry = tkinter.Entry(
    info_frame, bg=greay_grey, fg=light_green, font=my_font, borderwidth=3, width=10)
connect_button = tkinter.Button(
    info_frame, text="Connect", bg=light_green,  font=my_font, borderwidth=5, width=10, command=lambda: connect(my_connection))
disconnect_button = tkinter.Button(
    info_frame, text="Disconnect", bg=light_green,  font=my_font, borderwidth=5, width=10, state=DISABLED, command=lambda: disconnect(my_connection))

name_label.grid(row=0, column=0, padx=2, pady=10)
name_entry.grid(row=0, column=1, padx=2, pady=10)
port_label.grid(row=0, column=2, padx=2, pady=10)
port_entry.grid(row=0, column=3, padx=2, pady=10)
ip_label.grid(row=1, column=0, padx=2, pady=5)
ip_entry.grid(row=1, column=1, padx=2, pady=5)
connect_button.grid(row=1, column=2, padx=4, pady=5)
disconnect_button.grid(row=1, column=3, padx=4, pady=5)

# Color Frame Layout

color = StringVar()
color.set(white)
color_label = tkinter.Label(
    color_frame, text="Choose a color:", bg=greay_grey, fg=light_green, font=my_font)

white_button = tkinter.Radiobutton(
    color_frame, text="White", variable=color, value=white, bg=greay_grey, fg=light_green, font=my_font)
orange_button = tkinter.Radiobutton(
    color_frame, text="Orange", variable=color, value=orange, bg=greay_grey, fg=light_green, font=my_font)
pink_button = tkinter.Radiobutton(
    color_frame, text="Pink", variable=color, value=pink, bg=greay_grey, fg=light_green, font=my_font)
blue_button = tkinter.Radiobutton(
    color_frame, text="Blue", variable=color, value=blue, bg=greay_grey, fg=light_green, font=my_font)
yellow_button = tkinter.Radiobutton(
    color_frame, text="Yellow", variable=color, value=yellow, bg=greay_grey, fg=light_green, font=my_font)
purple_button = tkinter.Radiobutton(
    color_frame, text="Purple", variable=color, value=purple, bg=greay_grey, fg=light_green, font=my_font)
color_buttons = [white_button, orange_button, pink_button,
                 blue_button, yellow_button, purple_button]


white_button.grid(row=1, column=1, padx=2, pady=2)
orange_button.grid(row=1, column=2, padx=2, pady=2)
pink_button.grid(row=1, column=4, padx=2, pady=2)
blue_button.grid(row=1, column=5, padx=2, pady=2)
yellow_button.grid(row=1, column=6, padx=2, pady=2)
purple_button.grid(row=1, column=7, padx=2, pady=2)
color_label.grid(row=1, column=0, padx=2, pady=2)

# Output Frame Layout

my_scrollbar = tkinter.Scrollbar(output_frame, orient=VERTICAL)
my_listbox = tkinter.Listbox(output_frame, height=20, width=45, yscrollcommand=my_scrollbar.set,
                             bg=greay_grey, fg=light_green, font=my_font, borderwidth=3)
my_scrollbar.config(command=my_listbox.yview)

my_listbox.grid(row=0, column=0)
my_scrollbar.grid(row=0, column=1, sticky="NS")

# Input Frame Layout

input_entry = tkinter.Entry(
    input_frame, bg=greay_grey, fg=light_green, font=my_font, borderwidth=3, width=45)
send_button = tkinter.Button(
    input_frame, text="Send", bg=light_green, font=my_font, width=10, state=DISABLED, borderwidth=5, command=lambda: send_message(my_connection))
input_entry.grid(row=0, column=0, padx=5)
send_button.grid(row=0, column=1, padx=5)


# Create a Connection instance and pass it to the GUI

my_connection = Connection()
root.mainloop()
