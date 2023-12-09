import tkinter as tk
import socket
import threading
import json
from tkinter import DISABLED, END, NORMAL, VERTICAL


# Define Window
root = tk.Tk()
root.title("Chat Server")
root.iconbitmap("icon.ico")
root.geometry("600x600")
root.resizable(0, 0)

# Define fonts and colors
my_font = ('SimSun', 14)
black = "#010101"
light_green = "#1fc742"
root.config(bg=black)

# Define functions


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
                         font=my_font, bg=light_green, fg=black, borderwidth=5)
end_button = tk.Button(connection_frame, text="End Server", font=my_font,
                       bg=light_green, fg=black, borderwidth=5, state=DISABLED)

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
                        font=my_font, bg=light_green, state=DISABLED)
input_entry.grid(row=0, column=0, padx=5, pady=5)
send_button.grid(row=0, column=1, padx=5, pady=5)

# Layout for the admin frame

message_button = tk.Button(admin_frame, text="Send PM", font=my_font,
                           bg=light_green, fg=black, borderwidth=5, state=DISABLED)
kick_button = tk.Button(admin_frame, text="Kick", font=my_font,
                        bg=light_green, fg=black, borderwidth=5, state=DISABLED)
ban_button = tk.Button(admin_frame, text="Ban", font=my_font,
                       bg=light_green, fg=black, borderwidth=5, state=DISABLED)

message_button.grid(row=0, column=0, padx=5, pady=5)
kick_button.grid(row=0, column=1, padx=5, pady=5)
ban_button.grid(row=0, column=2, padx=5, pady=5)

# Run root window's main loop

root.mainloop()
