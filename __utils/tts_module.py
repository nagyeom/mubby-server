import os
import urllib.request

# aws polly
from boto3 import client
from gtts import gTTS


# 어떻게 동작하는지 확인할 것
class TextToSpeech:
    def __init__(self):
        pass

    def text_to_speech(self, client_info, tts_api=None):
        output_tts = "output_tts.mp3"
        text = client_info['watson_response']

        if tts_api:
            if tts_api == "google":
                self.google_tts(text, output_tts)
            elif tts_api == "naver_clova":
                self.naver_tts(text, output_tts)
            elif tts_api == "aws_polly":
                self.aws_tts(text, output_tts)
            else:
                print("그런 건 없어 폴리 시켜줄게")
                self.aws_tts(text, output_tts)
        else:
            self.aws_tts(text)

    def google_tts(self, text, output_tts):
        language = 'ko'
        rec_tts = gTTS(text=text, lang=language, slow=False)
        print("Saving gTTS mp3")
        rec_tts.save(output_tts)

        return output_tts

    def naver_tts(self, text, output_tts):
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
            with open(output_tts, 'wb') as f:
                f.write(response_body)
        else:
            print("Error Code:" + rescode)

        return output_tts

    def aws_tts(self, text, output_tts):
        polly = client("polly", region_name="ap-northeast-2")

        response = polly.synthesize_speech(
            Text=text,
            OutputFormat="mp3",
            VoiceId="Seoyeon")

        stream = response.get("AudioStream")

        with open(output_tts, 'wb') as f:
            data = stream.read()
            f.write(data)
        print("Saving AWS-Polly TTS mp3")

        return output_tts