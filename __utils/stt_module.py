#-*- coding:utf-8 -*-

# [START import_libraries]
# 파일 삽입 부분이라서 제일 위에 써줘야 한다.
from __future__ import division

import re
import sys

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
# [END import_libraries]s

import speech_recognition as sr

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

class SpeechToText:
    def __init__(self):
        self.result_audio_stt = ""
        self.result_mic_stt = ""

    def audio_stt(self, filename):
        with sr.AudioFile(filename) as source:
            r = sr.Recognizer()
            audio = r.record(source)
            try:
                self.result_audio_stt = r.recognize_google(audio, show_all=False, language='ko_KR')
            except Exception as e:
                self.result_audio_stt = ''
                print(e)

        # print("USER >>", self.result_audio_stt)

        return self.result_audio_stt

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

    def listen_print_loop(self, responses):
        text = ''
        """Iterates through server responses and prints them.

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

    def streaming(self, comuni, client_record=None):
        if client_record is not None:
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
                        for content in comuni.get_data(client_record))

            responses = client.streaming_recognize(streaming_config, requests)

            # Now, put the transcription responses to use.
            text = self.listen_print_loop(responses)
            return text
