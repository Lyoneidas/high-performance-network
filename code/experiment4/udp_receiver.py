import socket,select
import time
import json

localhost = "127.0.0.1"
real_localhost = "192.168.137.1"
destination = "192.168.137.103"

s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s1.bind((localhost, 5005))
s2 = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
s2.bind((localhost, 5005))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((localhost, 3333))
s.listen(1)
conn,addr = s.accept()

# start = ''
# while start != "HELLO":
#     start = conn.recv(1024)

while True:
    print "start receiving"
    r, w, x = select.select([s1, s2], [], [])
    tt = time.time()
    for i in r:
        print i, i.recvfrom(131072)
    conn.send(str(tt))
    # conn.send(str(tt))
