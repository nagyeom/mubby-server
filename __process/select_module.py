import multiprocessing
import select
from _thread import start_new_thread

# 시간을 나타내기 위해서 사용
import time
# file 및 dir 존재 유무를 판단하기 위해서 사용
import os
# 무삐의 기본 동작에 필요한 함수들이 다 들어가 있다.
import __utils.mubby_processor as mubby
from __utils.voice_thread import voice_thread


class SocketProcess(multiprocessing.Process):
    def __init__(self):
        super(SocketProcess, self).__init__()
        self.socket_process = None

    def run(self):
        self.socket_process = Handler()
        self.socket_process.handler()


class Handler:
    def __init__(self):
        self.connection_list = [mubby.server.getting_server()]

        print(" SERVER is running {}".format('-'*10))

        # 에이브릴 커넥터, 구글 등 객체 생성은 여기서 하도록 한다.

    def handler(self):
        while self.connection_list:
            # 로그로 수정해야하는 부분
            print("-")
            try:
                read_sock, write_sock, error_sock = select.select(self.connection_list, [], [], 5)
                # 이 경우를 실패했을 때는 어떻게 해야하지? 오류를 반환해야하나? 프로그램을 새로 시작해야 하나?

                for sock in read_sock:
                    # 처음 커넥션을 시도한 부분
                    if sock == self.connection_list[0]:
                        # < If select find new client >
                        client, client_ip = self.connection_list[0].accept()
                        # 원래는 에이브릴을 생성해서 넣어주었다.
                        self.connection_list.append(client)
                        print("{} >> new client {} connected".format(time.ctime(), client_ip))

                        # 사용자 ip를 기준으로 폴더를 생성하는 부분
                        # 이부분도 함수화 해야하지 않을까 싶다.
                        mubby.make_user_dir(client_ip[0])

                    # 커넥션 이후 동작 수행을 위한 함수 호출
                    else:
                        # 구분자에 따라 어떤 thread 를 생성할 것인지 결정 한다.
                        start_new_thread(voice_thread, (sock,))

                        # < If select find old client >
                        # 실제는 이하 부분을 thread 로 돌리던지 해야 정확하게 비동기가 진행될 것 같다.
                        # 각 try 별로 isSuccess 를 달아서 실패하면 더 이상 동작하지 않게 해야할 것 같다.
                        # 이하 내용을 client = 1 class 형식으로 담아서 주고 받아야 하지 않을까 싶다.
                        #
                        # try:
                        #     # < The server received data from client >
                        #     input_audio_path = mubby.pcm2wav(sock)
                        # except Exception as e:
                        #     print('\t★ default function error >> {}'.format(e))
                        #
                        # try:
                        #     # 음성 파일을 다운 받은 뒤에 stt, aibril 를 다녀와야 하기 때문에
                        #     # default 동작을 하는 함수를 불러와야 한다.
                        #     print("input_audio_path >> {} ".format(input_audio_path))
                        #     header, text, language = mubby.default(input_audio_path)
                        # except Exception as e:
                        #     print('\t★ default function error >> {}'.format(e))
                        #
                        # try:
                        #     print("header >> {}\ntext >> {}\nlanguage >> {}".format(header, text, language))
                        #     # < What should the server do? >
                        #     # Aibril 의 header.command 를 이용하여 어떤 동작을 할 것인지 정한다.
                        #     # 함수명 동작을 하는 함수를 불러와야 한다.
                        #     # def 함수명(command, text, language)
                        #     # return wave_file_path
                        #
                        #     # 하위 부분( - - - 까지) mubby_function 에 기능부분으로 만들어서 넣고 호출만 할 것.
                        #     if header['command'] == "chat":
                        #         # tts 에 다녀온다.
                        #         output_audio_path = mubby.chat_func(sock, text)
                        #
                        #     elif header['command'] == "weather":
                        #         # aibril 과 대화를 한 번 더 하고 tts 에 다녀온다.
                        #         output_audio_path = mubby.weather_func()
                        #
                        #     elif header['command'] == "music":
                        #         # (현재)
                        #         # tts 에 다녀오고
                        #         # 파일을 합치고 나서 반환한다.
                        #         # ps. 클라이언트와 상의해보고 동작방법을 바꿔야 할 수도 있다.
                        #         output_audio_path = mubby.music_func()
                        #     # - - -
                        #     else:
                        #         print("기본 음성 들어가게 해야하는데ㅔㅔㅔㅔㅔ")
                        #         # 잘못된 접근이라는 것을 알려주어야 한다.
                        #
                        # except Exception as e:
                        #     print('\t★ 함수명 function error >> {}'.format(e))
                        #
                        # try:
                        #     # < The server sent data to client >
                        #     # 음성 파일을 돌려주어야 한다. (확인)
                        #     # output_audio_path = "__user_audio/"+sock.getpeername()[0] + "/output_tts.wav"
                        #     print("out_audio_path >> {}".format(output_audio_path))
                        #     mubby.server.sending_wav(sock, output_audio_path)
                        # except Exception as e:
                        #     print('\t★ __send function error >> {}'.format(e))
                        #
                        # # (테스트용 모피) 한 동작 후 연결을 끊기 때문에 소켓 종료가 들어가야 서버가 여러번 정상동작을 할 수 있다.
                        # mubby.server.closing(sock)
                        #
                        # # 종료 쓰레드였다면 close 하고 소켓을 목록에서 삭제한다.
                        self.connection_list.remove(sock)

            except Exception as e:
                print('\t★ Program error >> {}'.format(e))