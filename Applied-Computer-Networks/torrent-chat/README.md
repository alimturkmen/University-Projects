# torrent-chat

Tested with Python3. 

Server and client have been tested in Windows and Ubuntu. In small files it is working well, but when it is time for big files some of the packets are getting lost on the way. We have implemented flow control sliding window protocol but there is no go-back-n mechanism for lost packets. 

### Usage:
Client should be started first. Because as soon as server has been started it is starting to send packets to the written address. And make sure that first packet is not lost. If it is lost client is throwing an error.

`python3 client.py`

`python3 server.py [address] [file-path]`

### Contributors:

- Alim Türkmen
- Enes Koşar
- Korhan Çağın Geboloğlu
