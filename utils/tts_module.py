# -*- coding:utf-8 -*-

from gtts import gTTS
import urllib.request
import os

class TextToSpeech:
    def __init__(self):
        self.output_gtts = "output_gtts.mp3"
        self.output_ntts = "output_ntts.mp3"

    def google_tts(self, text):
        language = 'ko'
        rec_tts = gTTS(text=text, lang=language, slow=False)
        print("Saving GOOGLE TTS mp3")
        rec_tts.save(self.output_gtts)

        return self.output_gtts

    def naver_tts(self, text):
        client_id = os.getenv('naver_tts_client_id')
        client_secret = os.getenv('naver_tts_client_secret')
        encText = urllib.parse.quote(text)
        data = "speaker=mijin&speed=0&text=" + encText
        url = "https://openapi.naver.com/v1/voice/tts.bin"

        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request, data=data.encode('utf-8'))
        rescode = response.getcode()

        if (rescode == 200):
            print("Saving Naver TTS mp3")
            response_body = response.read()
            with open(self.output_ntts, 'wb') as f:
                f.write(response_body)
        else:
            print("Error Code:" + rescode)

        return self.output_ntts
