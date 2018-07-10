import multiprocessing
# 시간을 나타내기 위해서 사용

from _thread import start_new_thread

# file 및 dir 존재 유무를 판단하기 위해서 사용
# 무삐의 기본 동작에 필요한 함수들이 다 들어가 있다.
from __configure.client_info import *
from __configure.mubby_value import CLIENT, CLIENT_LIST, REQUEST_ADDR
from __function.default import *
from __utils.socket_module import Socket
from __utils.action_thread import action_thread


class RequestProcess(multiprocessing.Process):
    def __init__(self):
        super(RequestProcess, self).__init__()
        self.__request_process = None

    def run(self):
        self.__request_process = Handler()
        self.__request_process.handler()

        # 한 문장으로 만들고 Handler
        # self.__request_process = Handler()


class Handler:
    def __init__(self):
        self.__request_socket = Socket(REQUEST_ADDR).getting_server()

        print(" SERVER is running {}".format('-'*10))

        # 에이브릴 커넥터, 구글 등 객체 생성은 여기서 하도록 한다.
        # 커넥팅 되고 난 다음에 class 넣어 저장하도록 해야한다.

    def handler(self):
        while self.__request_socket:
            # client_info 초기화
            client_info = CLIENT.copy()
            # 로그로 수정해야하는 부분
            print("-")
            try:
                # 01. First connect for setting request_socket_from_client
                request_socket_from_client, client_ip = self.__request_socket.accept()

                client_info['request_socket_from_client'] = request_socket_from_client
                make_user_dir(client_ip[0])
                print('client ip > {}'.format(client_ip[0]))
                print('client_info ip > {}'.format(client_info['request_socket_from_client'].getpeername()[0]))

                # 02. Comparison a client_serial_number and DB_records
                #   - if the same : return primary key
                primary_key = 'db-result'
                #       >> Add a new client_info at CLIENT_LIST
                CLIENT_LIST[primary_key] = ClientInfo(client_info)
                #
                #   - else: insert it than return the primary key
                #
                primary_key = 'db-result'
                CLIENT_LIST[primary_key]['request_socket_from_client'] = request_socket_from_client

                # 03. Start thread
                start_new_thread(action_thread, (CLIENT_LIST[primary_key],))

            except Exception as e:
                self.__request_socket = None
                print('\t★ RequestProcess error >> {}'.format(e))

            finally:
                pass
                # HAVE TO SAVE A CLIENT_LIST VALUE
                # YOU CAN USE A "PICKLE" MODULE
