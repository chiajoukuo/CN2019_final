import socket
import cv2
import numpy
import sys
import pyaudio
import threading
import subprocess
import wave
import time
import argparse


class Video_Server(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port 
        # self.conn = conn
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('[Video] New server socket thread started for '+self.ip+': '+str(self.port))
    
    def __del__(self):
        self.socket.close()
        try:
            cv2.destroyAllWindows()
        except:
            pass

    def run(self):
        self.video = cv2.VideoCapture("./MU_1.mp4")
        print('[Video] Start sending video frame to client...')
        self.socket.bind((self.ip, self.port))
        self.socket.listen(True)

        conn, addr = self.socket.accept()
        print("remote VEDIO client success connected...")

        # Read first frame.
        ok, frame = self.video.read()
        if not ok:
            print ('Cannot read video file')
            sys.exit()
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]

        while ok:
            result, imgencode = cv2.imencode('.jpg', frame, encode_param)
            data = numpy.array(imgencode)
            stringData = data.tostring()

            conn.send( (str(len(stringData)).ljust(16)).encode())
            conn.send( stringData )

            # ret, frame = capture.read()
            ok, frame = self.video.read()
            decimg=cv2.imdecode(data,1)
            cv2.imshow('SERVER2',decimg)
            cv2.waitKey(30)
            k = cv2.waitKey(1) & 0xff
            if k == 27 : break

CHUNK = 1024

class Audio_Server(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port 
        self.p = pyaudio.PyAudio()
        print('[Audio] New server socket thread started for '+self.ip+': '+str(self.port))
    def __del__(self):
        try:
            self.stream.stop_stream()
            self.stream.close()
        except:
            pass
        self.p.terminate()
    def run(self):
        command = "ffmpeg -i "+r"C:\Users\ariel\Desktop\lun\NTU\MU_1.mp4"+ " -ab 160k -ac 2 -ar 44100 -vn "+r"C:\Users\ariel\Desktop\lun\NTU\audio.wav"
        subprocess.call(command, shell=True)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(True)

        wf = wave.open('../../../audio.wav', 'rb') # should be different wav
        self.stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                input=True)

        print('[Audio] Start sending pyaudio configuration to client...')
        conn, addr = self.socket.accept()
        conn.send("sending pyaudio configuration".encode())
        conn.send(("configuration: "+str(self.p.get_format_from_width(wf.getsampwidth()))+' '+str(wf.getnchannels())+' '+str(wf.getframerate())).encode())
        time.sleep(1)
        conn.send("done".encode())

        flag_send_audio = False
        while flag_send_audio == False:
            data = conn.recv(1024).decode()
            if data == "done":
                flag_send_audio = True
        # read data
        data = wf.readframes(CHUNK)

        # send stream
        while len(data) > 0:
            # stream.write(data)
            conn.send(data)
            data = wf.readframes(CHUNK)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8000)
    print("Starting...")
    args = parser.parse_args()

    send_video = Video_Server(args.ip, args.port)
    send_audio = Audio_Server(args.ip, args.port+1)

    send_video.start()
    send_audio.start()