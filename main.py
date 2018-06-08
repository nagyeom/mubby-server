# -*- coding:utf-8 -*-

from utils import aibril_conv_module
from utils import stt_module
from utils import tts_module
from utils import audio_converter
from utils import wavefile_sending
from ffmpy import FFmpeg
import socket
import struct
import os

import time

from utils import module_communication

HOST = ''
PORT = 5555
ADDR = (HOST, PORT)
BUFF_SIZE = 1024

ST_PROTO_RECORD = 0x04
ST_PROTO_RECORD_DATA = 0x05
ST_PROTO_RECORD_PAUSE = 0x02
ST_PROTO_RECORD_STOP = 0x01

serverSocket = socket.socket()
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(ADDR)
serverSocket.listen(5)

aibril_conn = aibril_conv_module.WatsonServer()
stt_conn = stt_module.SpeechToText()
tts_conn = tts_module.TextToSpeech()
wave = wavefile_sending.WaveFile()


def pcm2wav(path):
    ff = FFmpeg(
            inputs={path: ['-f', 's16le', '-ar', '16000', '-ac', '2']},
            outputs={''.join([path, '.wav']): '-y'})
    ff.run()


def handler(clientSocket, addr, communi):
    print("Connected from", addr)

    f = open('record', 'wb')
    # print('ST_PROTO_RECORD_DATA')
    buf = clientSocket.recv(1024)
    print("buf {} ".format(buf))

    # << File receiving >>
    if buf == b'rec':
        start = time.time()
        while True:
            buf = clientSocket.recv(1024)
            if buf[-3:] == b'end':
                # print('ST_PROTO_RECORD_STOP')
                f.write(buf[:-3])
                f.close()
                file_recv_time = time.time() - start

                # << Pcm to Wave Converter >>
                start = time.time()
                pcm2wav('record')
                os.unlink('record')
                pcm_to_wav_time = time.time() - start
                break
            f.write(buf)

        # << google STT >>
        RECV_FILE = "record.wav"
        start = time.time()
        result_audio_stt = stt_conn.audio_stt(RECV_FILE)
        stt_time = time.time()-start
        User = result_audio_stt

        # << Aibril conversation >>
        start = time.time()
        result_conversation = aibril_conn.aibril_conv(result_audio_stt)
        aibril_time = time.time()-start
        Mubby = result_conversation

        # << awsPolly TTS >>
        start = time.time()
        tts_conn.aws_tts(result_conversation)
        aws_tts_time = time.time()-start

        # << mp3 to Wave Converter >>
        start = time.time()
        SEND_FILE = audio_converter.convert("output_atts.mp3")
        convert_time = time.time()-start

        start = time.time()
        with open(SEND_FILE, 'rb') as f:
            data = f.read()
        # print("size >> {}".format(len(data)))
        clientSocket.send(str(len(data)).encode())
        a = clientSocket.recv(1024)
        # print("recv{}".format(a))
        communi.sending_wav(clientSocket, SEND_FILE)
        what = clientSocket.recv(1024)
        file_send_time = time.time()-start
        clientSocket.close()

        return {"User": User, "Mubby": Mubby, "file_recv_time": file_recv_time, "pcm_to_wav_time": pcm_to_wav_time, "stt_time": stt_time, "aibril_time": aibril_time, "aws_tts_time": aws_tts_time, "convert_time": convert_time, "file_send_time": file_send_time}


def __print(dic):
    print("\n{}".format('= = ' * 10))
    print("{} >> {}".format("User", dic["User"]))
    print("{} >> {}".format("Mubby", dic["Mubby"]))
    print("{}".format('- - '*10))
    print("{} : {}".format("file_recv_time", dic["file_recv_time"]))
    print("{} : {}".format("pcm_to_wav_time", dic["pcm_to_wav_time"]))
    print("{} : {}".format("stt_time", dic["stt_time"]))
    print("{} : {}".format("aibril_time", dic["aibril_time"]))
    print("{} : {}".format("aws_tts_time", dic["aws_tts_time"]))
    print("{} : {}".format("convert_time", dic["convert_time"]))
    print("{} : {}".format("file_send_time", dic["file_send_time"]))
    print("{}".format('= = ' * 10))


if __name__ == '__main__':
    while True:
        # print('\nServer is running {}'.format('-'*5))
        communi = module_communication.Communication()
        clientSocket, addr = serverSocket.accept()
        times = handler(clientSocket, addr, communi)
        __print(times)
