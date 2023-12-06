# Client Side GUI for the chat application
import tkinter
import socket
import threading
from tkinter import DISABLED, VERTICAL, END

# Define Window
root = tkinter.Tk()
root.title("Chat Application")
root.iconbitmap("icon.ico")
root.geometry("700x700")
root.resizable(0, 0)


# Define Fonts and Colors

my_font = ("Arial", 14)
black = "#010101"
light_green = "#7ed957"
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
    pass


def disconnect():
    ''' Disconnects from the server. '''
    pass


def send():
    ''' Sends message to the server. '''
    pass


def receive():
    ''' Receives messages from the server. '''
    pass


# Define GUI Layout
# Create Frames
info_frame = tkinter.Frame(root, bg=black)
output_frame = tkinter.Frame(root, bg=black)
input_frame = tkinter.Frame(root, bg=black)

info_frame.pack()
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
    info_frame, text="Disconnect", bg=light_green,  font=my_font, borderwidth=5, width=10, state=DISABLED)

name_label.grid(row=0, column=0, padx=2, pady=10)
name_entry.grid(row=0, column=1, padx=2, pady=10)
port_label.grid(row=0, column=2, padx=2, pady=10)
port_entry.grid(row=0, column=3, padx=2, pady=10)
ip_label.grid(row=1, column=0, padx=2, pady=5)
ip_entry.grid(row=1, column=1, padx=2, pady=5)
connect_button.grid(row=1, column=2, padx=4, pady=5)
disconnect_button.grid(row=1, column=3, padx=4, pady=5)

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
    input_frame, text="Send", bg=light_green, font=my_font, width=10, state=DISABLED)
input_entry.grid(row=0, column=0, padx=5, pady=5)
send_button.grid(row=0, column=1, padx=5, pady=5)


# Define Main Loop

root.mainloop()
