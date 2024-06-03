import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import socket
import threading
import requests
import emoji
import sqlite3

SERVER = '127.0.0.1'
PORT = 12345
BUFFER_SIZE = 1024
FORMAT = 'utf-8'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_to_server():
    try:
        client_socket.connect((SERVER, PORT))
        threading.Thread(target=receive_messages).start()
    except ConnectionRefusedError:
        messagebox.showerror("Error", "Server is not running.")

def send_message(event=None):
    message = entry_field.get()
    msg_list.insert(tk.END, f"You: {message}")  # Display the input message in the listbox
    message = emoji.emojize(message)
    client_socket.send(message.encode(FORMAT))
    store_message('main_room', 'user', message)
    entry_field.delete(0, tk.END)

def receive_messages():
    while True:
        try:
            message = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
            msg_list.insert(tk.END, message)
        except OSError:
            break

def store_message(room_id, sender_id, message):
    conn = sqlite3.connect('chat_app.db')
    c = conn.cursor()
    c.execute("INSERT INTO messages (room_id, sender_id, message) VALUES (?, ?, ?)", (room_id, sender_id, message))
    conn.commit()
    conn.close()

def upload_file():
    file_path = file_entry.get()
    if file_path:
        try:
            with open(file_path, 'rb') as f:
                response = requests.post('http://127.0.0.1:5000/upload', files={'file': f})
            messagebox.showinfo("Success", response.text)
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
    else:
        messagebox.showerror("Error", "Please provide a file path.")

root = tk.Tk()
root.title("Chat Application")

style = ttk.Style()
style.theme_use('clam')

messages_frame = tk.Frame(root)
msg_list = tk.Listbox(messages_frame, height=15, width=50, font=('Helvetica', 12))
scrollbar = tk.Scrollbar(messages_frame, orient=tk.VERTICAL, command=msg_list.yview)
msg_list.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
messages_frame.pack(pady=10, padx=10)

entry_frame = tk.Frame(root)
entry_field = tk.Entry(entry_frame, width=50, font=('Helvetica', 12))
entry_field.bind("<Return>", send_message)
entry_field.pack(side=tk.LEFT, padx=(0, 5))
send_button = tk.Button(entry_frame, text="Send", command=send_message, font=('Helvetica', 12))
send_button.pack(side=tk.LEFT)
entry_frame.pack(pady=5)

file_frame = tk.Frame(root)
file_entry = tk.Entry(file_frame, width=50, font=('Helvetica', 12))
file_entry.pack(side=tk.LEFT, padx=(0, 5))
upload_button = tk.Button(file_frame, text="Upload", command=upload_file, font=('Helvetica', 12))
upload_button.pack(side=tk.LEFT)
file_frame.pack(pady=5)

connect_to_server()
root.mainloop()
