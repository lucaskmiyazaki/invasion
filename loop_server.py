import selectors
import socket
import threading
import time
import random
import re

HOST = '0.0.0.0'
PORT = 50007

command = 'ls'
clients = {}

def accept(sock, mask):
    global clients
    conn, addr = sock.accept()
    ip, port = addr
    id = random.randint(1000, 9999)
    print("connected to client: %d, ip: %s, port: %d "%(id, ip, port))
    conn.setblocking(False)
    #conn.send(command.encode())
    sel.register(conn, selectors.EVENT_READ, read)
    clients[id] = conn

def read(conn, mask):
    data = conn.recv(1000)
    if data:
        print(data.decode())
    else:
        sel.unregister(conn)
        conn.close()

def listen_from_terminal():
    global command
    while True:
        user_input = input("")
        reg = re.match("id\s*(?P<id>\d{4})\s*:\s*(?P<cmd>.*)", user_input)
        try:
            id = reg.group('id')
            command = reg.group('cmd')
            clients[int(id)].send(command.encode())
        except:
            print("type a valid command")

def still_alive(conn):
    try:
        conn.send(b'healthcheck')
        return True
    except:
        return False

def health_check():
    while True:
        time.sleep(1)
        for k in clients:
            if not still_alive(clients[k]):
                print("%d disconnected"%k)
                del clients[k]
                break

sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(100)
sock.setblocking(False)

sel = selectors.DefaultSelector()
sel.register(sock, selectors.EVENT_READ, accept)

task_lt = threading.Thread(target = listen_from_terminal)
task_lt.start()

task_hc = threading.Thread(target = health_check)
task_hc.start()

while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
