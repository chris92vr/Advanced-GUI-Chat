
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
    pass


def gui_start(connection):
    '''Starts the GUI for the chat application'''
    pass


def gui_end(connection):
    '''Ends the GUI for the chat application'''
    pass


def create_message(flag, name, message, color):
    '''Creates a JSON message to be sent to the clients'''
    pass


def process_message(connection, message_json):
    '''Update client based on message packet flag'''
    pass


def send_message(connection, message_json):
    '''Sends a message to the server'''
    pass


def receive_message(connection):
    '''Receives a message from the server'''
    pass


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
    info_frame, text="Connect", bg=light_green,  font=my_font, borderwidth=5, width=10, command=lambda: connect(my_connection))
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
    input_frame, text="Send", bg=light_green, font=my_font, width=10, state=DISABLED, borderwidth=5, command=send_message)
input_entry.grid(row=0, column=0, padx=5)
send_button.grid(row=0, column=1, padx=5)


# Create a Connection instance and pass it to the GUI

my_connection = Connection()
root.mainloop()
