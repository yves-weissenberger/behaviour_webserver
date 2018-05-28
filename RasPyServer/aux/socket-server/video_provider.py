import io
import socket
import struct
import time
import picamera
import fcntl
import time
import os

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


def get_task_start_time():
    try:
        with open("/home/pi/task_time.txt",'r') as f:
            temp = f.readline()
    except IOError:
        temp = time.time()
        print("Warning no task running, using recording start as reference")
    return float(temp)

piIp = get_ip_address('wlan0')
piId = str(int(piIp[-3:])-100)
st = get_task_start_time()


class SplitFrames(object):
    def __init__(self, connection):
        self.connection = connection
        self.stream = io.BytesIO()
        self.count = 0

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # Start of new frame; send the old one's length
            # then the data
            size = self.stream.tell()
            if size > 0:
                print time.time()
                self.connection.write(struct.pack('<f', (time.time()-st)))
                self.connection.flush()
                self.stream.seek(0)

                self.connection.write(struct.pack('<L', size))
                self.connection.flush()
                self.stream.seek(0)
                self.connection.write(self.stream.read(size))
                self.count += 1
                self.stream.seek(0)
        self.stream.write(buf)

client_socket = socket.socket()
client_socket.connect(('192.168.0.38', 8000+int(piId)))
connection = client_socket.makefile('wb')
with open("/home/pi/curr_pid.txt", 'w') as f:
    f.write(str(os.getpid()))
try:
    output = SplitFrames(connection)
    with picamera.PiCamera(resolution=(640,480), framerate=15) as camera:
        time.sleep(2)
        start = time.time()
        camera.start_recording(output, format='mjpeg')
        camera.wait_recording(1e12)  #this is more time than will ever be required to run
        camera.stop_recording()
        # Write the terminating 0-length to the connection to let the
        # server know we're done
        connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()
    finish = time.time()
print('Sent %d images in %d seconds at %.2ffps' % (
    output.count, finish-start, output.count / (finish-start)))

