#-*- coding:utf-8 -*-

import speech_recognition as sr
import os

from gtts import gTTS
# 아마존 TTS
from boto3 import client
# 제이슨
import urllib.request


class SpeechToText:
    def __init__(self, file_name, stt_api=None):
        self.output_stt = ""

        if stt_api:
            if stt_api == "google":
                self.google_stt(file_name)
            elif stt_api == "google_streaming":
                self.google_stt_streaming(file_name)
            else:
                print("그런 건 없어 스트리밍 시켜줄게")
                self.google_stt_streaming(file_name)
        else:
            self.google_stt_streaming(file_name)

    def google_stt(self, file_name):
        print("file_name >> {}".format(file_name))

        with sr.AudioFile(file_name) as source:
            r = sr.Recognizer()
            audio = r.record(source)
            try:
                self.output_stt = r.recognize_google(audio, show_all=False, language='ko_KR')
                print("Success Google STT")
            except Exception as e:
                print("Google STT false >> {}".format(e))

        print("self.output_stt >> {}".format(self.output_stt))

        return self.output_stt

    def google_stt_streaming(self, file_name):
        # 동작 가져와아아아아아아아아아아아아ㅏ하
        # 소켓 정보도 받아와야 한다 음하하하하
        pass


# 어떻게 동작하는지 확인할 것
class TextToSpeech:
    def __init__(self, text, tts_api=None):
        self.output_tts = "output_tts.mp3"

        if tts_api:
            if tts_api == "google":
                self.google_tts(text)
            elif tts_api == "naver_clova":
                self.naver_tts(text)
            elif tts_api == "aws_polly":
                self.aws_tts(text)
            else:
                print("그런 건 없어 폴리 시켜줄게")
                self.aws_tts(text)
        else:
            self.aws_tts(text)

    def google_tts(self, text):
        language = 'ko'
        rec_tts = gTTS(text=text, lang=language, slow=False)
        print("Saving gTTS mp3")
        rec_tts.save(self.output_tts)

        return self.output_tts

    def naver_tts(self, text):
        client_id = os.getenv('naver_tts_client_id')
        client_secret = os.getenv('naver_tts_client_secret')
        encText = urllib.parse.quote(text)
        data = "speaker=mijin&speed=0&text=" + encText
        url = "https://naveropenapi.apigw.ntruss.com/voice/v1/tts"

        request = urllib.request.Request(url)
        request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
        request.add_header("X-NCP-APIGW-API-KEY", client_secret)
        response = urllib.request.urlopen(request, data=data.encode('utf-8'))
        rescode = response.getcode()

        if rescode == 200:
            print("Saving Naver-Clova TTS mp3")
            response_body = response.read()
            with open(self.output_tts, 'wb') as f:
                f.write(response_body)
        else:
            print("Error Code:" + rescode)

        return self.output_tts

    def aws_tts(self, text):
        polly = client("polly", region_name="ap-northeast-2")

        response = polly.synthesize_speech(
            Text=text,
            OutputFormat="mp3",
            VoiceId="Seoyeon")

        stream = response.get("AudioStream")

        with open(self.output_tts, 'wb') as f:
            data = stream.read()
            f.write(data)
        print("Saving AWS-Polly TTS mp3")

        return self.output_tts


if __name__ == "__main__":
    name = "../__user_audio/192.168.0.1/record.wav"
    s = SpeechToText()
    a = s.google_stt(name)
