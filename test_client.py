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


class Video_Client(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket.socket()
        print('[Video] New client socket starting...')
    
    def __del__(self):
        self.socket.close()
        try:
            cv2.destroyAllWindows()
        except:
            pass

    def run(self):
        self.socket.connect((self.ip, self.port))
        print('[Video] receive video frame from server...')
        while 1:
            length = self.recvall(self.socket, 16)
            stringData = self.recvall(self.socket, int(length))
            data = numpy.fromstring(stringData, dtype='uint8')
            decimg=cv2.imdecode(data,1)
            cv2.imshow('CLIENT2',decimg)
            cv2.waitKey(1)

            k = cv2.waitKey(1) & 0xff
            if k == 27 : break

    def recvall(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

SIZE = 1024
CHUNK = 1024

class Audio_Client(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket.socket()
        self.p = pyaudio.PyAudio()
        print('[Audio] New client socket starting...')
    
    def __del__(self):
        self.socket.close()
        try:
            self.stream.stop_stream()
            self.stream.close()
        except:
            pass
        self.p.terminate()

    def run(self):
        self.socket.connect((self.ip, self.port))

        flag_start_play = False
        while flag_start_play == False:
            data = self.socket.recv(1024).decode()
            if data[:13] == "configuration":
                config = data.split()
                FORMAT = int(config[1])
                CHANNELS = int(config[2])
                RATE = int(config[3])
                print('[Audio] configuration', FORMAT, CHANNELS, RATE)
            elif data == "done":
                flag_start_play = True
                self.socket.send("done".encode())

        self.stream = self.p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)
        print('[Audio] Start receiving audio frame from server...')
        while flag_start_play == True:
            data = self.socket.recv(SIZE)
            if data:
                self.stream.write(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8000)
    print("Starting...")
    args = parser.parse_args()

    recv_video = Video_Client(args.ip, args.port)
    recv_audio = Audio_Client(args.ip, args.port+1)

    recv_video.start()
    recv_audio.start()