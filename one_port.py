# -*- coding:utf-8 -*-

from __utils import aibril_conv_module
from __utils import stt_module
from __utils import tts_module
from __utils import audio_converter
from __utils import wavefile_sending
from ffmpy import FFmpeg
import socket
import struct
import os

import time

from __utils import module_communication

HOST = ''
PORT = 5555
ADDR = (HOST, PORT)
BUFF_SIZE = 1024

ST_PROTO_RECORD = 0x04
ST_PROTO_RECORD_DATA = 0x05
ST_PROTO_RECORD_PAUSE = 0x02
ST_PROTO_RECORD_STOP = 0x01


def pcm2wav(path, chennal):
    ff = FFmpeg(
            inputs={path: ['-f', 's16le', '-ar', '16000', '-ac', chennal]},
            outputs={''.join([path, '.wav']): '-y'})
    ff.run()


def handler(clientSocket, addr, communi):
    print("Connected from", addr)

    # << google STT - Streaming>>
    start = time.time()
    result_audio_stt = stt_conn.streaming(communi, clientSocket)
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
    print("size >> {}".format(len(data)))
    answer = clientSocket.recv(1024)
    if answer == b'tel':
        clientSocket.send(str(len(data)).encode())
        a = clientSocket.recv(1024)
        # print("recv{}".format(a))
        communi.sending_wav(clientSocket, SEND_FILE)
        what = clientSocket.recv(1024)
        file_send_time = time.time()-start
        clientSocket.close()

    # pcm2wav('1channel_record', '1')
    pcm2wav('2channel_record', '1')

    return {"User": User, "Mubby": Mubby, "stt_time": stt_time, "aibril_time": aibril_time, "aws_tts_time": aws_tts_time,
            "convert_time": convert_time, "file_send_time": file_send_time}


def __print(dic):
    print("\n{}".format('= = ' * 10))
    print("{} >> {}".format("User", dic["User"], 2))
    print("{} >> {}".format("Mubby", dic["Mubby"], 2))
    print("{}".format('- - '*10))
    print("{} : {}".format("stt_time", dic["stt_time"], 2))
    print("{} : {}".format("aibril_time", dic["aibril_time"], 2))
    print("{} : {}".format("aws_tts_time", dic["aws_tts_time"], 2))
    print("{} : {}".format("convert_time", dic["convert_time"], 2))
    print("{} : {}".format("file_send_time", dic["file_send_time"], 2))
    print("{}".format('= = ' * 10))


if __name__ == '__main__':

    try:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    except:
        print('\nPlease set GOOGLE_APPLICATION_CREDENTIALS')
        print('{}'.format('- ' * 30))
        print('  $ export GOOGLE_APPLICATION_CREDENTIALS=[json PATH]')
        print('{}'.format('- ' * 30))
        exit(1)
    # pcm2wav('1channel_record', '1')
    # pcm2wav('2channel_record', '2')
    # pcm2wav('2channel_stereo.raw')

    serverSocket = socket.socket()
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(ADDR)
    serverSocket.listen(5)

    aibril_conn = aibril_conv_module.WatsonServer()
    stt_conn = stt_module.SpeechToText()
    tts_conn = tts_module.TextToSpeech()
    wave = wavefile_sending.WaveFile()

    while True:
        # print('\nServer is running {}'.format('-'*5))
        communi = module_communication.Communication()
        clientSocket, addr = serverSocket.accept()
        clientSocket.settimeout(5)
        clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
        times = handler(clientSocket, addr, communi)
        __print(times)