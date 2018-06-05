# -*- coding: utf-8 -*-
import struct
from random import *
import os

FILEINFO = [
    '병원놀이하자',
    '고양이소리',
    '루돌프방울소리',
    'BGM-2분30초',
    '머리가아파요',
    '환자할래'
]


class WaveFile:
    def __init__(self):
        self.sock = None
        self.filename = None

    def set_sock(self, sock, file_name):
        self.sock = sock
        self.filename = file_name
        #number = randint(0, 5)
        #self.filename = "audio/test_file"+str(number)+".wav"
        #print('\n\t{} size >> {}'.format(FILEINFO[number], os.path.getsize(self.filename)))

    def without_header(self):
        count = 0
        with open(self.filename, "br") as wave_file:
            print('\nwave file header and payload separated')
            header = wave_file.read(44)
            # w_file = wave_file.read()

            s = struct.unpack('i', header[40:])
            print("\t- data size info in header >> ", s[0])
            print("\t- count >> ", s[0]/8192)
            # print('\t- data size info, using len method >> ', len(w_file))

            while True:
                data = wave_file.read(8192)
                if len(data) == 0:
                    break
                count += 1
                print('\t- data len >> ', len(data))
                print('\t- data count >> ', count)
                if not self.send_file(data):
                    break

    def include_header(self):
        count = 0
        # print('\ninclue_header \tfile name > {}'.format(self.filename))
        # print('dire ? ', os.path.dirname(self.filename))
        with open(self.filename, "rb") as wave_file:
            print('\n\nwave file header not separated')
            # w_file = wave_file.read()
            # print('\t- data size info, using len method >> ', len(w_file))

            while True:
                data = wave_file.read(8192)
                if len(data) == 0:
                    break
                count += 1
                print('\t- data len >> ', len(data))
                print('\t- data count >> ', count)
                if not self.send_file(data):
                    break

    def send_file(self, data):
            self.sock.send(data)
            answer = self.sock.recv(1024)
            print('re_answer > {}'.format(answer))

            if answer:
                return True
            else:
                return False
