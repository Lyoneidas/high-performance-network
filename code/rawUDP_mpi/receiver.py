import socket,select
import sys,getopt
import commands
from mpi4py import MPI

def raw_listener(ip,port,tcpport,s1,s2):

    s1.bind((ip, port))

    s2.bind((ip, port))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("192.168.137.1", tcpport))
    s.listen(1)
    conn,addr = s.accept()
    while True:
        print "start receiving"
        r, w, x = select.select([s1, s2], [], [])
        tt = time.time()
        for i in r:
            print i, i.recvfrom(131072)
            conn.send(str(tt))

def main(argv):
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    host = commands.getoutput("hostname")
    s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s2 = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    # handler A
    if(rank == 0):
        print "{} starts listening".format(str(host))
        raw_listener("192.168.137.101",3335,3333,s1,s2)
    # handler B
    elif(rank == 1):
        print "{} starts listening".format(str(host))
        raw_listener("192.168.137.102",3335,3334,s1,s2)
    # controller
    elif(rank == 2):
        print "{} starts listening".format(str(host))
        print "{} not doing anything".format(str(host))




if __name__ == "__main__":
    main(sys.argv[1:])
