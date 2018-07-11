import multiprocessing
import select
# 시간을 나타내기 위해서 사용
import time

from _thread import start_new_thread

# file 및 dir 존재 유무를 판단하기 위해서 사용
# 무삐의 기본 동작에 필요한 함수들이 다 들어가 있다.
from __configure.client_info import *
from __function.default import *
from __utils.action_thread import action_thread


class AlarmProcess(multiprocessing.Process):
    def __init__(self):
        super(AlarmProcess, self).__init__()
        self.__alarm_process = None

    def run(self):
        self.__alarm_process = Handler()
        self.__alarm_process.handler()


"""
    수정해야 한다.
    알람 전용 프로세스로 -> 서버 송신 전용
"""


class Handler:
    def __init__(self):
        self.connection_list = [server.getting_server()]

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
                    # 01. First connect for setting request_socket_from_client
                    if sock == self.connection_list[0]:
                        client, client_ip = self.connection_list[0].accept()

                    # 02. Second connect for setting alarm_socket_to_client
                    if sock == self.connection_list[1]:
                        client, client_ip = self.connection_list[1].accept()

                        # 02. Comparison a client_serial_number and DB_records
                        #   - if the same : return primary key
                        #   - else: insert it than return the primary key
                        #

                        # 03.


                        self.connection_list.append(client)
                        print("{} >> new client {} connected".format(time.ctime(), client_ip))

                        # 사용자 ip를 기준으로 폴더를 생성하는 부분
                        make_user_dir(client_ip[0])

                    # 커넥션 이후 동작 수행을 위한 함수 호출
                    else:
                        # 구분자에 따라 어떤 thread 를 생성할 것인지 결정 한다.

                        # client data 를 받아와서 넘겨야 한다.
                        start_new_thread(client_thread, (sock,))
                        self.connection_list.remove(sock)

            except Exception as e:
                print('\t★ Program error >> {}'.format(e))