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
from _thread import start_new_thread

from utils import module_communication
addr = 1
HOST = ''
PORT = 5555
PORT2 = 5556
ADDR = (HOST, PORT)
ADDR2 = (HOST, PORT2)
BUFF_SIZE = 1024

server_recoder = socket.socket()
server_recoder.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_recoder.bind(ADDR)
server_recoder.listen(5)

server_speaker = socket.socket()
server_speaker.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_speaker.bind(ADDR2)
server_speaker.listen(5)

aibril_conn = aibril_conv_module.WatsonServer()
stt_conn = stt_module.SpeechToText()
tts_conn = tts_module.TextToSpeech()
wave = wavefile_sending.WaveFile()


def pcm2wav(path):
    ff = FFmpeg(
            inputs={path: ['-f', 's16le', '-ar', '16000', '-ac', '2']},
            outputs={''.join([path, '.wav']): '-y'})
    ff.run()


def handler(client_recoder, client_speaker,  addr, communi):
    print("Connected from", addr)
    ff = addr+"record"
    f = open(ff, 'wb')
    # print('ST_PROTO_RECORD_DATA')
    buf = client_recoder.recv(1024)
    print("buf {} ".format(buf))

    # << File receiving >>
    if buf == b'rec':
        start = time.time()
        while True:
            buf = client_recoder.recv(1024)
            print("buf >> {}".format(buf))
            if buf[-3:] == b'end':
                # print('ST_PROTO_RECORD_STOP')
                f.write(buf[:-3])
                f.close()
                file_recv_time = time.time() - start

                # << Pcm to Wave Converter >>
                start = time.time()
                pcm2wav(ff)
                os.unlink(ff)
                pcm_to_wav_time = time.time() - start
                break
            f.write(buf)

        # << google STT >>
        RECV_FILE = addr+"record.wav"
        start = time.time()
        result_audio_stt = stt_conn.audio_stt(RECV_FILE)
        stt_time = time.time()-start
        User = result_audio_stt
        # time.sleep(4)

        # << Aibril conversation >>
        start = time.time()
        result_conversation = aibril_conn.aibril_conv(result_audio_stt)
        aibril_time = time.time()-start
        Mubby = result_conversation
        # time.sleep(1)

        # << awsPolly TTS >>
        start = time.time()
        tts_conn.aws_tts(result_conversation, addr)
        aws_tts_time = time.time()-start
        # time.sleep(1)

        # << mp3 to Wave Converter >>
        start = time.time()
        OUT = addr+"output_atts.mp3"
        SEND_FILE = audio_converter.convert(OUT, addr)
        print("file name >> {}".format(SEND_FILE))
        convert_time = time.time()-start
        # time.sleep(1)

        # << Send to Client >>
        start = time.time()
        with open(SEND_FILE, 'rb') as f:
            data = f.read()
        print("size >> {}".format(len(data)))
        answer = client_speaker.recv(1024)
        if answer == b'tel':
            client_speaker.send(str(len(data)).encode())
            a = client_speaker.recv(1024)
            # print("recv{}".format(a))
            communi.sending_wav(client_speaker, SEND_FILE)
            what = client_speaker.recv(1024)
            file_send_time = time.time()-start

            client_recoder.close
            client_speaker.close

            return {"User": User, "Mubby": Mubby, "file_recv_time": file_recv_time, "pcm_to_wav_time": pcm_to_wav_time,
                    "stt_time": stt_time, "aibril_time": aibril_time, "aws_tts_time": aws_tts_time,
                    "convert_time": convert_time, "file_send_time": file_send_time}


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
        communi = module_communication.Communication()
        client_recoder, addr = server_recoder.accept()
        client_speaker, addr = server_speaker.accept()
        times = handler(client_recoder, client_speaker, str(addr[0]), communi)
        __print(times)
