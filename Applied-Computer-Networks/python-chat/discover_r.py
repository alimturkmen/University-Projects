import socket 
import os


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
HOST = s.getsockname()[0]
PORT = 5000
s.close()

u_name = input("Please enter a name. \n")

while True:
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		s.listen()
		conn, addr = s.accept()
		with conn:
			print('Connected by', addr)
			while True:
				msg = conn.recv(1024)
				if not msg:
					break
				msg = msg.decode()
				type = msg.split(';')[0]

				if type == '0':
					ip = msg.split(';')[1]
					name = msg.split(';')[2]
					dis_msg = '1;' + HOST + ';' + u_name + ';' + ip + ';' + name

					try:
						file = open('ip_name_list', 'a')
					except:
						file = open('ip_name_list', 'w')

					file2 = open('ip_name_list', 'r')
					content = file2.read()

					if ip not in content:
						file.writelines(name+":"+ip +"\n")	
					else:
						print('already exists')

					file.close()
					file2.close()

					with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
						s2.settimeout(1)
						try:
							s2.connect((ip, PORT))
							s2.sendall(str.encode(dis_msg))
							s2.close()
						except:
							print ("Nobody @" + ip)

		s.close()
						
		