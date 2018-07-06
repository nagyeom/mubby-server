import os

from __utils import aibril_connector
from __utils import socket_module
from __utils import audio_converter

from __configure.mubby_value import *
from __utils.speech_module import *

aibril = aibril_connector.WatsonServer()
server = socket_module.Socket()


def understand_func(input_pcm):
    text = SpeechToText(input_pcm, 'google')
    header, text, language = aibril.aibril_conv(text)

    return header, text, language


def response_func(client_ip, text):
    speech_path = "__user_audio/" + client_ip + "/convert_audio" + EXTENSION

    speech_file_name = TextToSpeech(text, 'aws_polly')
    speech = audio_converter.convert(speech_file_name, speech_path)

    return speech


def make_user_dir(client_ip):
    if not os.path.exists('__user_audio/' + client_ip):
        print('\tmake {} dir'.format(client_ip))
        os.system('mkdir __user_audio/' + client_ip)


def pcm2wav(client):
    # print("client.getpeername()[0] >> {}".format(client.getpeername()[0]))
    path = "__user_audio/"+client.getpeername()[0]+"/input"

    input_file = open(path, 'wb')
    while True:
        data = server.recving(client)
        # print("data {}".format(data))
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
