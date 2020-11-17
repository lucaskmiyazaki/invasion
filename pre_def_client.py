import socket 
from subprocess import Popen, PIPE

HOST = 'localhost'
PORT = 50007
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #s.sendall(b'hello world')
    data = s.recv(1024)
    print('received', repr(data))
    args = data.split()
    process = Popen(args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    print(stdout)
    s.sendall(stdout)
