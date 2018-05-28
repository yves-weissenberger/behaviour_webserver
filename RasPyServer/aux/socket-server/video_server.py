import io
import socket
import struct
from PIL import Image
import sys
import time
import os
# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)

boxNr = sys.argv[1]
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000+int(boxNr)))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
base = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
base_save = os.path.join(base,'media','box_'+str(boxNr))
#base_save = '/home/rastamouse/Documents/Code/RasPyServer/mysite/getData/static/getData/ims'
try:
    st = time.time() 
    nIms = len(os.listdir(base_save)) 
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        timestamp = struct.unpack('<f', connection.read(struct.calcsize('<f')))[0]
        #timestamp = nIms
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        image = Image.open(image_stream)

        #print('Image is %dx%d' % image.size)
        fName = str(nIms) + '_' + str(timestamp).replace(".",'-') + '.jpg'
        image.save(os.path.join(base_save,fName),format='jpeg')
        #print('Image is verified')
        nIms += 1
        #print("n: %s" %nIms)
        #print("t: %s" %(time.time() - st))
finally:
    connection.close()
    server_socket.close()