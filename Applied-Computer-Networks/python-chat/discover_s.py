import socket 
import os
import time


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
HOST = s.getsockname()[0]
PORT = 5000
s.close()


div_list = HOST.split('.')
offset = div_list[3]
local = div_list[0]+'.'+div_list[1]+'.'+div_list[2]
name = input("Please enter a name. \n")

while True:
	for i in range(2, 254):

		dest_ip = local + '.' + str(i)
		dis_msg = '0;' + HOST + ';' + name + ';' + dest_ip + ';'
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.settimeout(1)
			try:
				s.connect((dest_ip, PORT))
				time.sleep(1)
				s.sendall(str.encode(dis_msg))
				s.close()
			except:
				print ("Nobody @" + dest_ip)
	
	time.sleep(60)
		


	