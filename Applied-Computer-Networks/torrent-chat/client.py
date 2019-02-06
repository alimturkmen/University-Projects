from socket import *
import sys
import select

host="0.0.0.0"
port = 9999
s = socket(AF_INET,SOCK_DGRAM)
s.bind((host,port))

addr = (host,port)
buf= 1500

data,addr = s.recvfrom(buf)
data = data.decode()
print ("Receiving File:",data.strip(), "From:", addr[0])
name, ext = data.strip().split('.')[:-1],data.strip().split('.')[-1]

data,addr = s.recvfrom(buf)

fileData = bytearray()

#Rate calculation
import time
start = time.time()
counter = 1
try:
    while(data):
        if time.time() - start > 60:
            start = time.time() - 60
            rate = counter*1500
            print(rate, 'bytes/min', end='\r')
        fileData.extend(data) # caching the file
        s.sendto(str(1).encode(),addr)
        s.settimeout(2)
        data,addr = s.recvfrom(buf)
        counter += 1

except timeout:
    f = open(''.join(name)+ "_dl." + ext,'wb')
    f.write(fileData)
    f.close()
    s.close()
    print ("File Downloaded")
