from socket import *
import sys
import select


host="0.0.0.0"
port = 9999
s = socket(AF_INET,SOCK_DGRAM)
s.bind((host,port))

addr = (host,port)
buf= 15000

data,addr = s.recvfrom(buf)

data = data.decode()
print ("Receiving File:",data.strip(), "From:", addr[0])
name, ext = data.strip().split('.')[:-1],data.strip().split('.')[-1]

data,addr = s.recvfrom(buf)
checksum = checksum(data)
fileData = bytearray()

import time
start = time.time()
init_time = start

counter = 1
data_size = buf
buff_count = 1

try:
	while(data):
		if time.time() - start > 1:
			start = time.time() 
			rate = counter*buf
			counter = 0
			print(rate/1024/1024*8, 'Mbps', end='\r')
			buff_count += 1			
		fileData.extend(data) # caching the file
		s.sendto(str(checksum).encode(),addr)
		s.settimeout(2)
		data,addr = s.recvfrom(buf)
		counter += 1
		end_time = time.time()
		data_size += buf

except timeout:
    f = open(''.join(name)+ "_dl." + ext,'wb')
    f.write(fileData)
    f.close()
    s.close()
    print ("File Downloaded")

    avg_rate = data_size / buff_count
    print('Average rate:', avg_rate/1024/1024*8, ' Mbps')
    print('Elapsed time:', end_time-init_time)
    print('Data size:', data_size)
    print('Error in rate:', (data_size/(end_time-init_time)-avg_rate)/avg_rate)
