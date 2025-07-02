import socket
import threading
import os

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('localhost', 8089))
serversocket.listen(5) # become a server socket, maximum 5 connections

def handle_client(conn, addr):
    request = conn.recv(1024).decode()

    try:
        path = request.split(' ')[1]
        if path == '/':
            path = '/Instagram.html'
        filepath = 'arquivos' + path

        if not os.path.exists(filepath):
            raise FileNotFoundError

        with open(filepath, 'rb') as f:
            content = f.read()

        header = "HTTP/1.1 200 OK\r\n"
        if filepath.endswith('.html'):
            header += "Content-Type: text/html\r\n"
        elif filepath.endswith('.jpg') or filepath.endswith('.jpeg'):
            header += "Content-Type: image/jpeg\r\n"
        header += f"Content-Length: {len(content)}\r\n\r\n"

        conn.sendall(header.encode() + content)

    except FileNotFoundError:
        msg = "<h1>404 Not Found</h1>"
        header = "HTTP/1.1 404 Not Found\r\n"
        header += "Content-Type: text/html\r\n"
        header += f"Content-Length: {len(msg)}\r\n\r\n"
        conn.sendall(header.encode() + msg.encode())

    conn.close()


while True:
    connection, address = serversocket.accept()
    thread = threading.Thread(target=handle_client, args=(connection, address))
    thread.start()