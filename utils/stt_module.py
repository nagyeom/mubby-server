#-*- coding:utf-8 -*-

# import speech_recognition as sr
import os
import io

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

import audio_converter as au

class SpeechToText:
    def __init__(self):
        self.result_audio_stt = ""
        self.result_mic_stt = ""

    # def audio_stt(self, filename):
    #     with sr.AudioFile(filename) as source:
    #         r = sr.Recognizer()
    #         audio = r.record(source)
    #         try:
    #             self.result_audio_stt = r.recognize_google(audio, show_all=False, language='ko_KR')
    #         except Exception as e:
    #             print(e)
    #
    #     # print("USER >>", self.result_audio_stt)
    #
    #     return self.result_audio_stt

    def mic_stt(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('Say something ...')
            audio = r.listen(source)
        try:
            self.result_mic_stt = r.recognize_google(audio, show_all=False, language='ko_KR')
        except LookupError:
            print('Could not understand audio')

        print("USER>>", self.result_mic_stt)

        return self.result_mic_stt

    def cloud_stt(self):
        # Instantiates a client
        client = speech.SpeechClient()

        # The name of the audio file to transcribe
        # file_name = os.path.join(
        #     os.path.dirname("../record.wav"),
        #     'resources',
        #     'audio.raw')

        # file_name = os.path.join(
        #     os.path.dirname("../record.wav"),
        #     'resources',
        #     'audio.raw')

        file_name = "../record.wav"
        file_name = au.convert(file_name)

        # Loads the audio into memory
        with io.open(file_name, 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='ko-KR')

        # Detects speech in the audio file
        response = client.recognize(config, audio)

        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))


if __name__ == "__main__":
    test =SpeechToText()
    test.cloud_stt()

