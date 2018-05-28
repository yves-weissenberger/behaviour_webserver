print("hello!")
import os
import time
import numpy as np
import requests as req
import socket
import fcntl
import struct
import billiard


# Initi timers
st = time.time()
sendT = time.time()
pT = time.time()


def get_ip_address(ifname):
    """ Function from 
        https://stackoverflow.com/questions/24196932/how-can-i-get-the-ip-address-of-eth0-in-python
        """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def send_data(load):

    headers = {'User-Agent': 'Mozilla/5.0'}
    link = 'http://192.168.0.38:8000/getData/' + pi_ID + '/get_PiData/'
    print("LINK1")
    print(link)
    #session = req.Session()
    #r1 = session.get(link,headers=headers)

    link1 = 'http://192.168.0.38:8000/getData/' + pi_ID + '/write_PiData/'


    payload = {'piData':load}
    #cookies = dict(session.cookies)
    req.post(link1,headers=headers,data=payload)
    return None


piIp = get_ip_address('wlan0')
pi_ID = str(int(piIp[-3:])-100)

sndLst = []
lickLst = []
with open("/home/pi/task_time.txt",'w') as f:
    f.write(str(st))


while 1:

    if ((time.time() - sendT) > 5.):
        print (time.time()- st,lickLst)
        sendT = time.time()
        sndStr = 'sndList:' + '-'.join([str(np.round(entry[0],decimals=3))+entry[1] for entry in sndLst])
        lickStr = 'LickList:' + '-'.join([str(np.round(entry[0],decimals=3))+entry[1] for entry in lickLst])
        sendStr = ','.join([sndStr,lickStr])
        print sendStr

        sendProc = billiard.Process(target=send_data,args=(sendStr,))
        sendProc.start()
        #send_data(sendStr)
        lickLst = []
        sndLst = []
        print("SEEEEENDING!",time.time() - st)
        print(((time.time() - sendT) > 5.))
    
    if ((time.time() - pT) > .1):
        print ("in",time.time()- st)
        if np.random.uniform(0,1)>.8:
            sndLst.append([time.time() - st,'L'])


        if (np.random.uniform(0,1)>.975):
            print "play_sound"
            sndLst.append([time.time() - st,'5'])
        pT = time.time()
