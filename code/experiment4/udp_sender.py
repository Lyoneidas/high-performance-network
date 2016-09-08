from socket import *
import struct,time

localhost = "127.0.0.1"
real_localhost = "192.168.137.1"
destination = "192.168.137.103"

tcp_socket = socket(AF_INET,SOCK_STREAM)
tcp_socket.connect((localhost,3333))

s = socket(AF_INET, SOCK_RAW, IPPROTO_UDP)
data = 'string'
sport = 4711    # arbitrary source port
dport = 5005   # arbitrary destination port
length = 8+len(data);
checksum = 0
udp_header = struct.pack('!HHHH', sport, dport, length, checksum)
# tcp_socket.send(str("HELLO"))
for i in range(0,10):
    print "into the loop"
    st = time.time()
    s.sendto(udp_header+data, (localhost, 0));
    data = tcp_socket.recv(1024)
    print st - float(data)
    time.sleep(1)

    # print data
    # time.sleep(1)
