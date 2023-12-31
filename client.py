# Client Side GUI for the chat application
import tkinter
import socket
import threading
from tkinter import DISABLED, VERTICAL, END, NORMAL, StringVar

# Define Window
root = tkinter.Tk()
root.title("Chat Application")
root.iconbitmap("icon.ico")
root.geometry("800x800")
root.resizable(0, 0)


# Define Fonts and Colors

my_font = ("Arial", 14)
black = "#010101"
light_green = "#7ed957"
white = "#ffffff"
light_gray = "#e8e8e8"
orange = "#ff862f"
dark_green = "#324930"
pink = "#ff0080"
blue = "#00bfff"
yellow = "#ffff00"
purple = "#800080"
root.config(bg=black)


# Define socket costants

ENCODER = "utf-8"
BYTESIZE = 1024
global client_socket  # Global socket variable (not a good practice)


# Define Functions

def connect():
    ''' Connects to the server. '''
    global client_socket

    # Clear any previous chat
    my_listbox.delete(0, END)

    # Get the required connection information
    name = name_entry.get()
    ip = ip_entry.get()
    port = port_entry.get()

    # Only try to make a connection if all three fields are filled in
    if name and ip and port:
        # Conditions for connection are met, try connection
        my_listbox.insert(
            0, f"{name} is waiting to connect to {ip} at {port}...")

        # Create aclient socket to connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, int(port)))

        # Verify that the connection is valid
        verify_connection(name)
    else:
        # Conditions were not met
        my_listbox.insert(0, "Insufficient information to connect")


def verify_connection(name):
    '''Verify that the server connection is valid and pass required information'''
    global client_socket

    # The server will send a NAME flag if a valid connection is made
    flag = client_socket.recv(BYTESIZE).decode(ENCODER)
    if flag == 'NAME':
        # The connection was made, send client name and await confirmation
        client_socket.send(name.encode(ENCODER))
        message = client_socket.recv(BYTESIZE).decode(ENCODER)

        if message:
            # Server sent a verification, connection is valid!
            my_listbox.insert(0, message)

            # Change button/entr states
            connect_button.config(state=DISABLED)
            disconnect_button.config(state=NORMAL)
            send_button.config(state=NORMAL)

            name_entry.config(state=DISABLED)
            ip_entry.config(state=DISABLED)
            port_entry.config(state=DISABLED)

            # Create a thread to continuosly receive a message from the server
            receive_thread = threading.Thread(target=receive)
            receive_thread.start()
        else:
            # No verification message was receive
            my_listbox.insert(0, "Connection not verified, GOODBYE!")
            client_socket.close()
    else:
        # No name flag was sent, connection refused
        my_listbox.insert(0, "Connection refused! Goodbye..")
        client_socket.close()


def disconnect():
    ''' Disconnects from the server. '''
    global client_socket

    # Close the client socket
    client_socket.close()

    # Change button/entry states
    connect_button.config(state=NORMAL)
    disconnect_button.config(state=DISABLED)


def send():
    ''' Sends message to the server. '''
    global client_socket

    # Send the message to the server
    message = input_entry.get()
    client_socket.send(message.encode(ENCODER))

    # Clear the input field
    input_entry.delete(0, END)


def receive():
    ''' Receives messages from the server. '''
    global client_socket

    while True:
        try:
            # Receive message from the server
            message = client_socket.recv(BYTESIZE).decode(ENCODER)
            my_listbox.insert(0, message)
        except:
            # An error occurred, close the client socket
            print("An error occurred, closing the client socket...", flush=True)
            my_listbox.insert(
                0, "An error occurred, closing the client socket...")
            disconnect()
            break


# Define GUI Layout
# Create Frames
info_frame = tkinter.Frame(root, bg=black)
color_frame = tkinter.Frame(root, bg=black)
output_frame = tkinter.Frame(root, bg=black)
input_frame = tkinter.Frame(root, bg=black)

info_frame.pack()
color_frame.pack()
output_frame.pack(pady=10)
input_frame.pack()

# Info Frame Layout

name_label = tkinter.Label(info_frame, text="Name:",
                           bg=black, fg=light_green, font=my_font)
name_entry = tkinter.Entry(
    info_frame, bg=black, fg=light_green, font=my_font, borderwidth=3)
ip_label = tkinter.Label(info_frame, text="Host IP:",
                         bg=black, fg=light_green, font=my_font)
ip_entry = tkinter.Entry(info_frame, bg=black,
                         fg=light_green, font=my_font, borderwidth=3)
port_label = tkinter.Label(info_frame, text="Port:",
                           bg=black, fg=light_green, font=my_font)
port_entry = tkinter.Entry(
    info_frame, bg=black, fg=light_green, font=my_font, borderwidth=3, width=10)
connect_button = tkinter.Button(
    info_frame, text="Connect", bg=light_green,  font=my_font, borderwidth=5, width=10, command=connect)
disconnect_button = tkinter.Button(
    info_frame, text="Disconnect", bg=light_green,  font=my_font, borderwidth=5, width=10, state=DISABLED, command=disconnect)

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
    color_frame, text="Choose a color:", bg=black, fg=light_green, font=my_font)

white_button = tkinter.Radiobutton(
    color_frame, text="White", variable=color, value=white, bg=black, fg=light_green, font=my_font)
light_gray_button = tkinter.Radiobutton(
    color_frame, text="Light Gray", variable=color, value=light_gray, bg=black, fg=light_green, font=my_font)
orange_button = tkinter.Radiobutton(
    color_frame, text="Orange", variable=color, value=orange, bg=black, fg=light_green, font=my_font)
dark_green_button = tkinter.Radiobutton(
    color_frame, text="Dark Green", variable=color, value=dark_green, bg=black, fg=light_green, font=my_font)
pink_button = tkinter.Radiobutton(
    color_frame, text="Pink", variable=color, value=pink, bg=black, fg=light_green, font=my_font)
blue_button = tkinter.Radiobutton(
    color_frame, text="Blue", variable=color, value=blue, bg=black, fg=light_green, font=my_font)
yellow_button = tkinter.Radiobutton(
    color_frame, text="Yellow", variable=color, value=yellow, bg=black, fg=light_green, font=my_font)
purple_button = tkinter.Radiobutton(
    color_frame, text="Purple", variable=color, value=purple, bg=black, fg=light_green, font=my_font)
color_buttons = [white_button, light_gray_button, orange_button, dark_green_button, pink_button,
                 blue_button, yellow_button, purple_button]


white_button.grid(row=1, column=0, padx=2, pady=2)
light_gray_button.grid(row=1, column=1, padx=2, pady=2)
orange_button.grid(row=1, column=2, padx=2, pady=2)
dark_green_button.grid(row=1, column=3, padx=2, pady=2)
pink_button.grid(row=1, column=4, padx=2, pady=2)
blue_button.grid(row=1, column=5, padx=2, pady=2)
yellow_button.grid(row=1, column=6, padx=2, pady=2)
purple_button.grid(row=1, column=7, padx=2, pady=2)
color_label.grid(row=0, column=3, padx=2, pady=2)

# Output Frame Layout

my_scrollbar = tkinter.Scrollbar(output_frame, orient=VERTICAL)
my_listbox = tkinter.Listbox(output_frame, height=20, width=45, yscrollcommand=my_scrollbar.set,
                             bg=black, fg=light_green, font=my_font, borderwidth=3)
my_scrollbar.config(command=my_listbox.yview)

my_listbox.grid(row=0, column=0)
my_scrollbar.grid(row=0, column=1, sticky="NS")

# Input Frame Layout

input_entry = tkinter.Entry(
    input_frame, bg=black, fg=light_green, font=my_font, borderwidth=3, width=45)
send_button = tkinter.Button(
    input_frame, text="Send", bg=light_green, font=my_font, width=10, state=DISABLED, borderwidth=5, command=send)
input_entry.grid(row=0, column=0, padx=5)
send_button.grid(row=0, column=1, padx=5)


# Define Main Loop

root.mainloop()
