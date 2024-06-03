import socket
import threading
from flask import Flask, request
from flask_socketio import SocketIO, emit
import sqlite3

# Initialize Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Database setup
conn = sqlite3.connect('chat_app.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users 
            (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS messages 
            (id INTEGER PRIMARY KEY, room_id TEXT, sender_id TEXT, message TEXT)''')

clients = []

def register(username, password):
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    return user is not None

def store_message(room_id, sender_id, message):
    c.execute("INSERT INTO messages (room_id, sender_id, message) VALUES (?, ?, ?)", (room_id, sender_id, message))
    conn.commit()

def get_message_history(room_id):
    c.execute("SELECT * FROM messages WHERE room_id=?", (room_id,))
    messages = c.fetchall()
    return messages

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(f'uploads/{file.filename}')
    return 'File uploaded successfully'

def handle_client(client_socket, address):
    while True:
        try:
            message = client_socket.recv(1024).decode()
        except ConnectionResetError:
            clients.remove(client_socket)
            client_socket.close()
            break

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 12345))
server_socket.listen(5)

def start_server():
    while True:
        client_socket, address = server_socket.accept()
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

# Run Flask and SocketIO
if __name__ == '__main__':
    threading.Thread(target=start_server).start()
    socketio.run(app, port=5000)
