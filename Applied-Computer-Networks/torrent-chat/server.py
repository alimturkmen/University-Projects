from socket import *
import sys, _thread, time

global rwnd
rwnd = 50 # sliding window size

# receive ack from client
def receiveAck(n):
	global rwnd
	data,addr = s.recvfrom(1500)
	while data:
		rwnd = rwnd + 1 # increment receive window by one, because we have got one ack
		data,addr = s.recvfrom(1500)

s = socket(AF_INET,SOCK_DGRAM)

host = sys.argv[1]
port = 9999
buf = 1500
addr = (host,port)


file_name=sys.argv[2]

s.sendto(file_name.encode(),addr)
	
f=open(file_name,"rb")
data = f.read(buf)

_thread.start_new_thread( receiveAck, (1,) )

while (data):
	if rwnd < 0:
		time.sleep(0.5)
	if(s.sendto(data,addr)):
		rwnd = rwnd - 1 # decrease by one because one packet is in flight.
		print (rwnd)
		data = f.read(buf)
s.close()
f.close()
