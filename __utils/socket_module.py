# 통신부분에 대한 것을 여기다 모아야 한다.
# 현재는 그냥 동작 돌 수 있도록 가져다 놓았다.
# 추후 수정 필요 꼭
# 커넥팅 후에 꼭!
# 꼬옥!
# 꼭!
import socket

# 아래 내용은 추후 setting file을 만들어서 거기에 setting value 들을 다 모아야 할 것 같다.
HOST = ''
PORT = 5555
ADDR = (HOST, PORT)
FILE_HEADER_SIZE = 44
FILE_READ_SIZE = 8192
BUF_SIZE = 1024


# 메시지 형태를 구분하는 구분자 역활 함수를 집어 넣어야 한다.
# app-text, app-voice, mubby-voice 등등..
class Socket:
    def __init__(self):
        self.__server = socket.socket()
        self.__server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__server.bind(ADDR)
        self.__server.listen(5)

    def getting_server(self):
        return self.__server
    #
    # def setting_sock(self, client):
    #     self.client = client

    def recving(self, client):
        # self.client.recv(BUF_SIZE)
        data = client.recv(BUF_SIZE)
        return data
        # 수신 후 해야 할 동작이 있는 경우 여기다가 작성 한다.

    def sending(self, client, data):
        # 받을 때 에러가 생기는 경우 대비를 해야할 것 같지 아니하지 않니..?
        # self.client.send(data)
        # answer = self.client.recv(BUF_SIZE)

        client.send(data)
        answer = client.recv(BUF_SIZE)
        print('here_re_answer > {}'.format(answer))

        if answer == b'ack' or answer == b'spk':
            return True
        else:
            return False

    def closing(self, client):
        client.close()

    def sending_wav(self, client, audio_path):

        answer = client.recv(BUF_SIZE)
        if answer == b'tel':
            with open(audio_path, "rb") as wave_file:
                data = wave_file.read()
                is_success = self.sending(client, str(len(data)).encode())

            if is_success:
                with open(audio_path, "rb") as wave_file:
                    count = 0
                    data = wave_file.read(FILE_HEADER_SIZE)
                    if self.sending(client, data):
                        while True:
                            data = wave_file.read(FILE_READ_SIZE)
                            if len(data) == 0:
                                break
                            else:
                                count += 1
                                print('\t- data len >> ', len(data))
                                print('\t- data count >> ', count)
                                if not self.sending(client, data):
                                    break




#
# class Communication:
#     def __init__(self):
#         self.sock = None
#
#     def setting_sock(self, sock):
#         self.sock = sock
#
#     def sending_wav(self, sock,  audios):
#         self.setting_sock(sock)
#
#         with open(audios, "rb") as wave_file:
#             count = 0
#             data = wave_file.read(44)
#             if self.sending(data):
#                 while True:
#                     data = wave_file.read(8192)
#                     if len(data) == 0:
#                         break
#                     else:
#                         count += 1
#                         print('\t- data len >> ', len(data))
#                         print('\t- data count >> ', count)
#                         if not self.sending(data):
#                             break
#
#     def sending(self, data):
#             self.sock.send(data)
#             answer = self.sock.recv(1024)
#             print('here_re_answer > {}'.format(answer))
#
#             if answer == b'ack':
#                 return True
#             else:
#                 return False
