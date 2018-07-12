import speech_recognition as sr
import os

from gtts import gTTS
# 아마존 TTS
from boto3 import client
# 제이슨
import urllib.request


class SpeechToText:
    def __init__(self):
        pass

    def speech_to_text(self, client_info, stt_api=None):
        file_name = client_info['stt_file_name']

        if stt_api:
            if stt_api == "google":
                self.google_stt(file_name)
            elif stt_api == "google_streaming":
                self.google_stt_streaming(file_name)
            else:
                print("그런 건 없어 스트리밍 시켜줄게")
                self.google_stt_streaming(client_info)
        else:
            self.google_stt_streaming(client_info)

    def google_stt(self, file_name):
        print("file_name >> {}".format(file_name))

        with sr.AudioFile(file_name) as source:
            r = sr.Recognizer()
            audio = r.record(source)
            try:
                output_stt = r.recognize_google(audio, show_all=False, language='ko_KR')
                print("Success Google STT")
            except Exception as e:
                print("Google STT false >> {}".format(e))

        print("self.output_stt >> {}".format(output_stt))

        return output_stt

    def listen_print_loop(self, responses):
        """
            Iterates through server responses and prints them.

            The responses passed is a generator that will block until a response
            is provided by the server.

            Each response may contain multiple results, and each result may contain
            multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
            print only the transcription for the top alternative of the top result.

            In this case, responses are provided for interim results as well. If the
            response is an interim one, print a line feed at the end of it, to allow
            the next result to overwrite it, until the response is a final one. For the
            final one, print a newline to preserve the finalized transcription.
        """
        text = ''
        num_chars_printed = 0
        for response in responses:
            if not response.results:
                continue

            # The `results` list is consecutive. For streaming, we only care about
            # the first result being considered, since once it's `is_final`, it
            # moves on to considering the next utterance.
            result = response.results[0]
            if not result.alternatives:
                continue

            # Display the transcription of the top alternative.
            transcript = result.alternatives[0].transcript

            # Display interim results, but with a carriage return at the end of the
            # line, so subsequent lines will overwrite them.
            #
            # If the previous result was longer than this one, we need to print
            # some extra spaces to overwrite the previous result
            overwrite_chars = ' ' * (num_chars_printed - len(transcript))

            if not result.is_final:
                sys.stdout.write(transcript + overwrite_chars + '\r')
                sys.stdout.flush()

                num_chars_printed = len(transcript)

            else:
                # print(transcript + overwrite_chars)
                text = transcript + overwrite_chars

                # Exit recognition if any of the transcribed phrases could be
                # one of our keywords.
                if re.search(r'\b(exit|quit)\b', transcript, re.I):
                    print('Exiting..')
                    break

                num_chars_printed = 0

        return text

    def google_stt_streaming(self, socket_action, client_info=None):
        if client_info is not None:
            # See http://g.co/cloud/speech/docs/languages
            # for a list of supported languages.
            language_code = 'ko-KR'  # a BCP-47 language tag

            # for content in comuni.get_data(client_record):
            #     print("Type >> {}".format(type(content)))

            client = speech.SpeechClient()
            config = types.RecognitionConfig(
                encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=RATE,
                language_code=language_code)
            streaming_config = types.StreamingRecognitionConfig(
                config=config,
                interim_results=True)
            requests = (types.StreamingRecognizeRequest(audio_content=content)
                        for content in socket_action.get_data(client_record))

            responses = client.streaming_recognize(streaming_config, requests)

            # Now, put the transcription responses to use.
            text = self.listen_print_loop(responses)
            return text


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


if __name__ == "__main__":
    name = "../__user_audio/192.168.0.1/record.wav"
    s = SpeechToText()
    a = s.google_stt(name)
