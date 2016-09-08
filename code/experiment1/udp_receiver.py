import socket
import time
import json

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

#start signal
sock_start = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock_start.bind(("192.168.137.103",3334))
start = ''

sock_time = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_STREAM) # UDP
sock_time.bind(("192.168.137.103",3336))
sock_time.listen(1)

#correct check and send back 1 or 0 for resend
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.137.103",3335))
s.listen(1)

periodTerm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
periodTerm.bind(("192.168.137.103",3337))
periodTerm.listen(1)

metrics = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
metrics.connect(("192.168.137.1",3333))



sock_recv = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock_recv.bind(("192.168.137.103",5005))

while start != "START":
    start = str(sock_start.recvfrom(1024)[0])

data = ''
print "start receiving"
conn, addr = s.accept()
end = ''
time_Read,adr_t = sock_time.accept()
p_signal,adr_p = periodTerm.accept()
endTimeList=[]
while end != "TERMINATE":
    correct = 0
    recvList = []
    size = 0
    size = int(conn.recv(1024))
    print "Receiving:",size
    start_time = float(time_Read.recv(1024))
    print "start time:",start_time
    start_time = time.time()
    while correct != 1:
        #get data
        data, addr = sock_recv.recvfrom(20)
        if(str(data) != "TERMINATE"):
            recvList.append(data)
        elif (str(data) == "TERMINATE"):
            # print "Get data:",recvList
            if(len(recvList) == size):
                end_time = time.time()
                print end_time - start_time
                endTimeList.append(end_time-start_time)
                conn.send(str(1))
                correct = 1
            else:
                conn.send(str(0))
                correct = 0
                recvList = []
    print "Check if everything is endded"
    end = p_signal.recv(1024)
    print "END:",end





trasn_d = json.dumps(endTimeList)

trans = chunkstring(trasn_d,512)
print "Start transmission to metrics"
for ele in trans:
    metrics.send(str(ele))
    time.sleep(0.01)
print "Transmission complete"
time.sleep(1)
metrics.send("TERMINATE")
data = metrics.recv(1024)
metrics.close()
print "received data:", data
