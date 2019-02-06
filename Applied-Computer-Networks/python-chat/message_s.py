import socket 
import hashlib

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
HOST = s.getsockname()[0]
PORT = 5001
s.close()

dest_name = input('To whom you want to chat? ')

file = open('ip_name_list', 'r')
content = file.readlines()
ip = ''

for tuple in content:
	name = tuple.split(':')[0]
	ip = tuple.split(':')[1].strip()
	if name == dest_name :
		break

file.close()

try:
	file = open('cypher/'+ip, 'r')
	cypher = file.read().strip()
	file.close()

except:
	file = open('cypher/'+ip, 'w')
	cypher = hashlib.md5(str.encode('alim')).hexdigest()
	file.write(cypher)

while True:
	msg = input('Your message: ')
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		
		file = open('cypher/'+ip, 'r')
		cypher = file.read().strip()
		file.close()

		s.settimeout(2)
		s.connect((ip, PORT))

		cypher = hashlib.md5(str.encode(cypher)).hexdigest()
		msg_s = HOST+';'+cypher+';'+msg
		s.sendall(str.encode(msg_s))
		s.close()

		file = open('cypher/'+ip, 'w')
		file.write(cypher)
		file.close()

		file = open('message/'+ip, 'a')
		file.write('You:'+msg+'\n')
		file.close()


