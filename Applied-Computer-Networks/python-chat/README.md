This is a very simple chat application written in python and uses sockets for the communication.

First run discover_r.py, then discover_s.py to learn the people and their IP addresses in the network. In order to send a message, use message_s.sh and always keep message_r.py running.

discover_s.py sends the machine's ip address to the rest of the machines in the local network. This takes approximately 5 minutes. Then waits for 1 minute and repeats the same process.

discover_r.py receives the ip addresses and the regarding names then stores this data in ip_name_list. 

message_r.py receives the messages and checks whether the sender is fraud or not using a cypher generated via md5 function. 

message_s.py allows user to send messages to the names that are discovered before.
