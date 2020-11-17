import selectors
import socket
import threading
import time

HOST = '0.0.0.0'
PORT = 50007

command = 'ls'

def accept(sock, mask):
    conn, addr = sock.accept()
    print("conected by ", addr)
    conn.setblocking(False)
    conn.send(command.encode())
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    data = conn.recv(1000)
    if data:
        print(data)
    else:
        sel.unregister(conn)
        conn.close()

def listen_from_terminal():
    global command
    while True:
        command = input("")

sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(100)
sock.setblocking(False)

sel = selectors.DefaultSelector()
sel.register(sock, selectors.EVENT_READ, accept)

thread = threading.Thread(target = listen_from_terminal)
thread.start()

while thread.is_alive():
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
