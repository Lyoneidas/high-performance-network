from socket import *
import struct,time

def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)

def checksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        w = ord(msg[i]) + (ord(msg[i+1]) << 8)
        s = carry_around_add(s, w)
    return ~s & 0xffff

tcpA = socket(AF_INET,SOCK_STREAM)
tcpA.connect((localhost,3333))

tcpB = socket(AF_INET,SOCK_STREAM)
tcpB.connect((localhost,3333))

s = socket(AF_INET, SOCK_RAW, IPPROTO_UDP)
data = 'string'
sport = 4711    # arbitrary source port
dport = 3335   # arbitrary destination port
length = 8+len(data);
checksum = 0
udp_header = struct.pack('!HHHH', sport, dport, length, checksum)

for i in range(0,10):
    print "into the loop"
    # send a
    st_A = time.time()
    real_checksum = checksum(udp_header+st_A)
    tcpA.send(real_checksum)
    s.sendto(udp_header+st_A, ("192.168.137.101", 0));
    data = tcpA.recv(1024)
    print st_A - float(data)
    time.sleep(0.001)
    # send b
    st_B = time.time()
    real_checksum = checksum(udp_header+st_B)
    tcpB.send(real_checksum)
    s.sendto(udp_header+data, ("192.168.137.102", 0));
    data = tcpB.recv(1024)
    print st_B - float(data)
    time.sleep(0.001)
