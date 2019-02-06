# WiFi Chat Report

- To run the program, one should run the following commands respectively:  
    - Firstly client should wait:  
    - `python3 client.py`  
    - Then server should start sending file to the destination:  
    - `python3 server.py DEST-IP FILE`
- Computer A is running Windows 10, Computer B is running Kali Linux 2018.3. 
- The tests were conducted in a very small home, this is why we haven't got drastical changes. Also all doors are half-to-half glass. In our opinion this has an effect on the results, too.
- We have tested the TCP rate by sending an receiving 1 GB file, with buffer size 15000 bytes. 
- In the Computer B it was always showing 72.2 Mbps when we have run the command `iwconfig wlan0` no matter where we are in home.
- In the Computer A, we have run the command `netsh wlan show interface`. When we run the command in the eduroam:

    Name                   : Wi-Fi  
    Description            : Dell Wireless 1820A 802.11ac  
    GUID                   : 1b91caad-6186-4c9a-93de-efbd0f8073a0  
    Physical address       : 74:df:bf:30:b5:ad  
    State                  : connected  
    SSID                   : eduroam  
    BSSID                  : ac:a3:1e:97:07:d1  
    Network type           : Infrastructure  
    Radio type             : 802.11ac  
    Authentication         : WPA2-Enterprise  
    Cipher                 : CCMP  
    Connection mode        : Profile  
    Channel                : 56  
    Receive rate (Mbps)    : 144  
    Transmit rate (Mbps)   : 360  
    Signal                 : 84%  
    Profile                : eduroam  
    
 - Receive and transmit rates were always equal to each other in the test area. This is why we have added signal ratio, too.

- These are the results we have come up with:

| pos. xmit | pos. rcv | PHY rate 1 | PHY rate 2 | iperf rate | TCP rate |
|-----------|---|---|---|---|---|
|A1|B1|144 Mbps (92%)|72.2 Mbps|25.1 Mbps|15.75 Mbps|
|B1|A1|72.2 Mbps|144 Mbps (92%)|20.1 Mbps|18.07 Mbps|
|A2|B2|144 Mbps (88%)|72.2 Mbps|22.3 Mbps|14.64 Mbps|
|B2|A2|72.2 Mbps|144 Mbps (88%)|19.3 Mbps|17.03 Mbps|
|A3|B3|144 Mbps (82%)|72.2 Mbps|19.2 Mbps|14.48 Mbps|
|B3|A3|72.2 Mbps|144 Mbps (82%)|17.9 Mbps|16.81 Mbps|

- This the sketch of the place where test are conducted:

![Figure 1](https://github.com/CMPE487/wifi-chat-alimturkmen/blob/master/home.png "Figure 1")

- Contributors are
  - Enes Koşar
  - Alim Türkmen
