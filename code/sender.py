

import socket

import sys,getopt

import random

import time

def toMetrics(data):
    sock_metrics = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock_metrics.sendto(data, ("192.168.137.1",5005))
    sock_metrics.sendto("TERMINATE",("192.168.137.1",5005))

def generateLostSequence(size,lostRate):
    sendQueue = getSequence(size)
    if(lostRate > 0.0):
        kickQueue = random.sample(range(0,size),int(float(size)*lostRate/100))
        for kick in kickQueue:
            sendQueue[kick]=-1
    # print "Send queue size:",str(len(filter(lambda a:a>=0,sendQueue)))
    return sendQueue

def getSequence(size):
    queue=[]
    for i in range(0,size):
        queue.append(i)
    return queue

def A_feed(sock,data):
    if(data != -1):
        sock.sendto(str(data),("192.168.137.101",3333))
        # sock.sendto(str(data),("127.0.0.1",3333))

def B_feed(sock,data):
    if(data != -1):
        sock.sendto(str(data),("192.168.137.102",3333))
        # sock.sendto(str(data),("127.0.0.2",3333))

def generalMode(size, lostRate):
    #General Scenario

    #Result with timestamp
    restTimestamp_A = []
    restTimestamp_B = []

    #UDP socket
    sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP

    #Get the queue
    queue_A = generateLostSequence(size,lostRate)
    queue_B = generateLostSequence(size,lostRate)
    for i in queue_A:
        A_feed(sock,i)
        restTimestamp_A.append({'value':i,'timeStamp':time.time()})
        time.sleep(0.001)
    A_feed(sock,"TERMINATE")

    time.sleep(0.01)

    for j in queue_B:
        B_feed(sock,j)
        time.sleep(0.001)
    B_feed(sock,"TERMINATE")

def reliableMode(size,lostRate):
    #A is always reliable
    sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
    queue_A = getSequence(size)
    queue_B = generateLostSequence(size, lostRate)
    for i in queue_A:
        A_feed(sock,i)
        time.sleep(0.001)
    time.sleep(0.01)
    for j in queue_B:
        B_feed(sock,j)
        time.sleep(0.001)

    A_feed(sock,"TERMINATE")
    B_feed(sock,"TERMINATE")

def main(argv):
    mode=''
    size=0
    lostRate=0.0
    defaultPort=3333
    ipMaster="192.168.137.103"
    ipRecv_A="192.168.137.101"
    ipRecv_B="192.168.137.102"

    #Get rumtime parameter
    try:
        opts,args= getopt.getopt(argv,"hm:s:r:",["mode=","size=","lostRate="])
    except getopt.GetoptError:
        print "sender.py -m <send model> -r <lost rate>"
        sys.exit(2)

    for opt, arg in opts:
        #Get help
        if opt == '-h':
            print "sender.py -m <send model> -r <lost rate>"
            sys.exit()
        #Get send mode
        elif opt in ("-m","--mode"):
            if(arg == "nl"):
                print "=======Send in No Data Lost Mode======"
            elif(arg == "dl"):
                print "=======Send in Random Data Lost Mode======"
            elif(arg == "rl"):
                print "=======Send in Reliable Mode======"
            else:
                print "ERROR::Mode selection invalid!"
                sys.exit(2)
            mode=arg
        #Get send size
        elif opt in ("-s","--size"):
            size = int(arg)
            if(size > 0 and size < 1024):
                print "Set datagram series size:", arg
            else:
                print "ERROR::Data size selection invalid"
                sys.exit(2)
        #Get data lost rate
        elif opt in ("-r","--lostRate"):
            lostRate = float(arg)
            if(mode == "nl"):
                lostRate = 0.0
            elif(lostRate > 100.0):
                print "ERROR::Lost rate selection invalid"
                sys.exit(2)
            print "Selected lost rate:"+str(lostRate)+"%"
    #Testing two functions
    # print "10 element queue:",getSequence(10)
    # print "10 element queue lost 2 elements",generateLostSequence(10,2.1)
    # print "10 element queue with no lost: ", generateLostSequence(10,0)

    #Start sending MESSAGE

    #send start signal
    sock_start = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock_start.sendto("START",("192.168.137.103",5005))
    sock_start.sendto("START",("192.168.137.102",5005))
    sock_start.sendto("START",("192.168.137.101",5005))
    sock_start.sendto("START",("192.168.137.1",5005))
    if(mode in ("nl","dl")):
        generalMode(size,lostRate)
    elif(mode == "rl"):
        reliableMode(size,lostRate)


if __name__ == "__main__":
    main(sys.argv[1:])



#Getting arguements
# print "==========================================="
# print "Dual data sender starts with configuration:"
# print "Send mode:",str(sys.argv[0])
#
#
# UDP_IP="127.0.0.1"
# UDP_PORT=3333

#
# for counter in range(0,100):
#     sock.sendto(str(counter),(UDP_IP,UDP_PORT))
#
# sock.sendto("TERMINATE",(UDP_IP, UDP_PORT))
#sock.sendto("Hello, master!", ("192.168.137.103",3333))

#Send to receiver A
#sock.sendto("Hello, receiver A!",("192.168.137.101",3333))

#Send to receiver B
#sock.sendto("Hello, receiver B!",("192.168.137.102",3333))

#sock.sendto("TERMINATE", ("192.168.137.103",3333))
#sock.sendto("TERMINATE", ("192.168.137.102",3333))
#sock.sendto("TERMINATE", ("192.168.137.101",3333))
