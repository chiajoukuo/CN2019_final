import cv2
import sys
import socket
import numpy

TCP_IP = "127.0.0.1"
TCP_PORT = 8002
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(True)
conn, addr = s.accept()

encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]

# Read video
video = cv2.VideoCapture("MU_1.mp4") 
# Exit if video not opened.
if not video.isOpened():
    print ("Could not open video")
    sys.exit() 
# Read first frame.
ok, frame = video.read()
if not ok:
    print ('Cannot read video file')
    sys.exit() 
while True:
    # Read a new frame
    ok, frame = video.read()
    if not ok:
        break
    # new
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    data = numpy.array(imgencode)
    stringData = data.tostring()
    conn.send( str(len(stringData)).ljust(16).encode())
    conn.send( stringData )

    # Display result
    cv2.imshow("Video Streaming", frame)
    # cv2.imwrite("./MU_1/"+nname+".jpg", frame)

    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27 : break

conn.close()
cv2.destroyAllWindows()

'''
ret, frame = capture.read()


while ret:
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    data = numpy.array(imgencode)
    stringData = data.tostring()

    conn.send( str(len(stringData)).ljust(16));
    conn.send( stringData );

    ret, frame = capture.read()
    decimg=cv2.imdecode(data,1)
    cv2.imshow('SERVER2',decimg)
    cv2.waitKey(30)



'''