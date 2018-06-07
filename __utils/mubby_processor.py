from __utils import speech_module
from __utils import aibril_connector
from __utils import audio_converter
from __utils import socket_module

import os

EXTENSION = ".wav"

stt = speech_module.SpeechToText()
tts = speech_module.TextToSpeech()
aibril = aibril_connector.WatsonServer()
server = socket_module.Socket()


def default(input_audio):
    text = stt.google_stt(input_audio)
    command, text, language = aibril.aibril_conv(text)
    # speech = tts.google_tts(text)
    # mubby_speech = audio_converter.convert(speech, path)

    return command, text, language


def chat_func(client, text):
    path = "__user_audio/" + client.getpeername()[0] + "/convert_audio" + EXTENSION

    speech = tts.google_tts(text)
    mubby_speech = audio_converter.convert(speech, path)

    return mubby_speech


def weather_func():
    print("구현중")
    # return 으로 준비중입니다 하나 만들기.


def music_func():
    print("구현중")
    # tts, 파일 함침 등등 해야함.. 귀찮..
    # return 으로 준비중입니다 하나 만들기.


def pcm2wav(client):
    # print("client.getpeername()[0] >> {}".format(client.getpeername()[0]))
    path = "__user_audio/"+client.getpeername()[0]+"/input"

    input_file = open(path, 'wb')
    while True:
        data = server.recving(client)
        print("data {}".format(data))
        if data[-3:] == b'end':
            print('ST_PROTO_RECORD_STOP')
            input_file.write(data[:-3])
            input_file.close()
            audio_converter.pcm2wav(path, EXTENSION)
            os.unlink(path)
            break
        input_file.write(data)

    # audio_converter.pcm2wav(path, EXTENSION)
    # os.unlink(path)

    return path+EXTENSION
