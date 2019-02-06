import socket 
import hashlib

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
HOST = s.getsockname()[0]
PORT = 5001
s.close()

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

				src = msg.split(';')[0]
				cypher = msg.split(';')[1]
				message = msg.split(';')[2].strip()

				file = open('ip_name_list', 'r')
				content = file.readlines()
				name = ''

				for tuple in content:
					name = tuple.split(':')[0]
					ip = tuple.split(':')[1].strip()
					if ip == src :
						break

				file.close()

				try:
					file = open('cypher/'+src, 'r')
					cypher2 = file.read().strip()
					cypher3 = hashlib.md5(str.encode(cypher2)).hexdigest()
					file.close()

					if cypher == cypher2 or cypher == cypher3:
						print(name+':'+message)
						file = open('cypher/'+src, 'w')
						file.write(cypher3)
						file.close()
						file = open('message/'+src, 'a')
						file.write(name+':'+message+'\n')
					else:
						print ('ALERT, CYPHER MISMATCH !!')
				except:
					file = open('cypher/'+src, 'w')
					file.write(cypher)
					file.close()
					file = open('message/'+src, 'a')
					file.write(name+':'+message+'\n')
					file.close()
		s.close()
		


