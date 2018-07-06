import multiprocessing
import select
from _thread import start_new_thread

# 시간을 나타내기 위해서 사용
import time
# file 및 dir 존재 유무를 판단하기 위해서 사용
# 무삐의 기본 동작에 필요한 함수들이 다 들어가 있다.
import __function.default as mubby
from __utils.voice_thread import client_thread


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
        # 커넥팅 되고 난 다음에 class 넣어 저장하도록 해야한다.

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
                        mubby.make_user_dir(client_ip[0])

                    # 커넥션 이후 동작 수행을 위한 함수 호출
                    else:
                        # 구분자에 따라 어떤 thread 를 생성할 것인지 결정 한다.
                        start_new_thread(client_thread, (sock,))
                        self.connection_list.remove(sock)

            except Exception as e:
                print('\t★ Program error >> {}'.format(e))