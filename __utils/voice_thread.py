from __function.default import *
from __function.music import *
from __function.weather import *


# < If select find old client >
# 실제는 이하 부분을 thread 로 돌리던지 해야 정확하게 비동기가 진행될 것 같다.
# 각 try 별로 isSuccess 를 달아서 실패하면 더 이상 동작하지 않게 해야할 것 같다.
# 이하 내용을 client = 1 class 형식으로 담아서 주고 받아야 하지 않을까 싶다.
def client_thread(sock):
    try:
        # < The server received data from client >
        input_audio_path = pcm2wav(sock)
    except Exception as e:
        print('\t★ default function error >> {}'.format(e))

    try:
        # 음성 파일을 다운 받은 뒤에 stt, aibril 를 다녀와야 하기 때문에
        # default 동작을 하는 함수를 불러와야 한다.
        print("input_audio_path >> {} ".format(input_audio_path))
        header, text, language = understand_func(input_audio_path)
    except Exception as e:
        print('\t★ default function error >> {}'.format(e))

    try:
        print("header >> {}\ntext >> {}\nlanguage >> {}".format(header, text, language))
        # < What should the server do? >
        # Aibril 의 header.command 를 이용하여 어떤 동작을 할 것인지 정한다.

        if header['command'] == "chat":
            # tts 에 다녀온다.
            output_audio_path = response_func(sock.getpeername()[0], text)

        elif header['command'] == "weather":
            # aibril 과 대화를 한 번 더 하고 tts 에 다녀온다.
            output_audio_path = weather_func()

        elif header['command'] == "music":
            # (현재)
            # tts 에 다녀오고
            # 파일을 합치고 나서 반환한다.
            # ps. 클라이언트와 상의해보고 동작방법을 바꿔야 할 수도 있다.
            output_audio_path = music_func()
        # - - -
        else:
            print("기본 음성 들어가게 해야하는데ㅔㅔㅔㅔㅔ")
            # 잘못된 접근이라는 것을 알려주어야 한다.

    except Exception as e:
        print('\t★ 함수명 function error >> {}'.format(e))

    try:
        # < The server sent data to client >
        # 음성 파일을 돌려주어야 한다. (확인)
        # output_audio_path = "__user_audio/"+sock.getpeername()[0] + "/output_tts.wav"
        print("out_audio_path >> {}".format(output_audio_path))
        server.sending_wav(sock, output_audio_path)
    except Exception as e:
        print('\t★ __send function error >> {}'.format(e))

        # 한 동작 후 연결을 끊어준다.
        server.closing(sock)