import selectors
import socket

HOST = '0.0.0.0'
PORT = 50007

def accept(sock, mask):
    conn, addr = sock.accept()
    print("conected by ", addr)
    conn.setblocking(False)
    conn.send(b'ls')
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    data = conn.recv(1000)
    if data:
        print(data)
    else:
        sel.unregister(conn)
        conn.close()

sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(100)
sock.setblocking(False)

sel = selectors.DefaultSelector()
sel.register(sock, selectors.EVENT_READ, accept)

while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
