from __utils import speech_module
from __utils import aibril_connector
from __utils import audio_converter


stt_conn = speech_module.SpeechToText()
tts_conn = speech_module.TextToSpeech()
aibril_conn = aibril_connector.WatsonServer

def func_mubby(input_audio):
    text = stt_conn.google_stt(input_audio)
    answer = aibril_conn.aibril_conv_connect(text)
    speech = tts_conn.google_tts(answer)
    mubby_speech = audio_converter.convert(speech)

    return mubby_speech
