import subprocess
import os
import sys
import argparse


def ping_box(box_nr):

    base_addr = '192.168.0.'
    box_addr = base_addr + str(100 + int(box_nr))

    cmd = ['fping','-t 300','-r 1',box_addr]
    #a = subprocess.check_output(cmd)
    #print(a)
    #print ("HELLO")
    try:
        a = subprocess.check_output(cmd)
        print(a)
        if 'alive' in str(a):
            is_active=1
    except:
        is_active = 0

    return is_active


if __name__=="__main__":

    
    #argparse.parse_args()
    box_nr = sys.argv[1]

    #proc1 = subprocess.Popen(['ssh','pi@192.168.0.' + str(box_nr), 'mkdir socket_video'],
    #    shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    cFP = os.path.abspath(__file__)

    fp = os.path.join(os.path.split(cFP)[0], "socket-server", "video_provider.py")
    print(fp)

    # scp syntax: scp foobar.txt your_username@remotehost.edu:/some/remote/directory 
    proc2 = subprocess.Popen(['scp',fp,'pi@192.168.0.' + str(box_nr)+":/home/pi/socket_video/video_provider.py"],
        shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    print(proc2.stderr.readlines())

