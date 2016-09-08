import socket
import time
import random

def generateLostSequence(size,lostRate):
    sendQueue = getSequence(size)
    if(lostRate > 0.0):
        sam = int(float(size)*lostRate/100.0)
        kickQueue = random.sample(range(0,size),sam)
        for kick in kickQueue:
            sendQueue[kick]=-1
    return sendQueue

def getSequence(size):
    queue=[]
    for i in range(0,size):
        queue.append(i)
    return queue

def sendSequence(seq, sock):
    for ele in seq:
        if str(ele) != "-1":
            sock.sendto(str(ele),("192.168.137.103",5005))
            time.sleep(0.001)
    sock.sendto("TERMINATE",("192.168.137.103",5005))


UDP_IP = "192.168.137.103"
UDP_PORT = 5005
#start signal
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto("START",(UDP_IP, 3334))

#expected result and get resend_flag
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.137.103",3335))

periodTerm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
periodTerm.connect(("192.168.137.103",3337))


sock_time = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_STREAM) # UDP
sock_time.connect(("192.168.137.103",3336))

for i in range(100,1000,10):
    print "Sending:",i
    resend_flag = 0
    s.send(str(i))
    sock_time.send(str(time.time()))
    resendTime = 0
    while resend_flag == 0:
        sequence = []
        if(resendTime < 30):
            lostRatio = random.uniform(0.0,3.2)
            sequence = generateLostSequence(i,lostRatio)
        else:
            sequence = getSequence(i)
        sendSequence(sequence,sock)
        resend_flag = int(s.recv(1024))
        resendTime+=1

    if( i == 990):
        periodTerm.send("TERMINATE")
    else:
        periodTerm.send("No")

# sock.sendto("TERMINATE", (UDP_IP, UDP_PORT))
