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
    #print("LINK1")
    #print(link)
    #session = req.Session()
    #r1 = session.get(link,headers=headers)

    link1 = 'http://192.168.0.38:8000/getData/' + pi_ID + '/write_PiData/'


    payload = {'piData':load}
    #cookies = dict(session.cookies)
    req.post(link1,headers=headers,data=payload)
    return None


piIp = get_ip_address('wlan0')
pi_ID = str(int(piIp[-3:])-100)

stimLst = []
respLst = []
optoLst = []
rewLst = []
corrLst = []
with open("/home/pi/task_time.txt",'w') as f:
    f.write(str(st))


while 1:

    if ((time.time() - sendT) > 5.):
        sendT = time.time()
        stimStr = 'stimList:' + '-'.join([str(np.round(entry[0],decimals=3))+entry[1] for entry in stimLst])
        respStr = 'respList:' + '-'.join([str(np.round(entry[0],decimals=3))+entry[1] for entry in respLst])
        rewStr = 'rewList:' + '-'.join([str(np.round(entry[0],decimals=3))+entry[1] for entry in rewLst])
        optoStr = 'optoList:' + '-'.join([str(np.round(entry[0],decimals=3))+entry[1] for entry in optoLst])
        corrStr = "corrList:" + '-'.join([str(i) for i in corrLst])

        sendStr = ','.join([stimStr,respStr,rewStr,optoStr,corrStr])
        #print sendStr

        sendProc = billiard.Process(target=send_data,args=(sendStr,))
        sendProc.start()
        #send_data(sendStr)
        stimLst = []
        respLst = []
        optoLst = []
        rewLst = []
        #print("SEEEEENDING!",time.time() - st)
        #print(((time.time() - sendT) > 5.))
    
    if ((time.time() - pT) > .1):
        #print ("in",time.time()- st)
        if np.random.uniform(0,1)>.8:
            if np.random.uniform(0.5)>.5:
                respLst.append([time.time() - st,'_L'])
            else:
                respLst.append([time.time() - st,'_R'])



        if (np.random.uniform(0,1)>.975):
            #print "play_sound"
            stimLst.append([time.time() - st,"_"+str(int(np.random.randint(0,6,size=1)))])
            if np.random.uniform(0,1)>.2:
                corrLst.append(1)

        if (np.random.uniform(0,1)>.975):
            if np.random.uniform(0.5)>.8:
                rewLst.append([time.time() - st,'_L'])
            else:
                rewLst.append([time.time() - st,'_R'])


        pT = time.time()
