import socket
import struct

from __configure.mubby_value import BUF_SIZE, FILE_HEADER_SIZE, FILE_READ_SIZE


class Socket:
    def __init__(self, address_port=None):
        if address_port:
            self.__server = socket.socket()
            self.__server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.__server.bind(address_port)
            self.__server.listen(5)
        else:
            print("에러에러 소켓 정의가 잘못 되었음")
            exit(1)

    def getting_server(self):
        return self.__server
    #
    # def setting_sock(self, client):
    #     self.client = client

    @staticmethod
    def setting_socket_option(client):
        client.settimeout(5)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))


class SocketAction:
    def __init__(self, client_info):
        self.__client = client_info['request_socket_from_client']
        self.__audio_path = client_info['folder_path']

    def receiving(self):
        data = self.__client.recv(BUF_SIZE)
        return data
        # 수신 후 해야 할 동작이 있는 경우 여기다가 작성 한다.

    def sending(self, data):
        # 받을 때 에러가 생기는 경우 대비를 해야할 것 같지 아니하지 않니..?
        # self.client.send(data)
        # answer = self.client.recv(BUF_SIZE)

        self.__client.send(data)
        answer = self.__client.recv(BUF_SIZE)
        # print('here_re_answer > {}'.format(answer))

        if answer == b'ack' or answer == b'spk':
            return True
        else:
            print('send end')
            self.__client.send(b'end')
            return False

    def closing(self):
        try:
            self.__client.close()
            return True
        except:
            return False

    def sending_wav(self, file_name):
        audio_path = self.__audio_path + file_name
        answer = self.receiving()
        if answer == b'tel':
            with open(audio_path, "rb") as wave_file:
                data = wave_file.read()
                is_success = self.sending(str(len(data)).encode())

            if is_success:
                with open(audio_path, "rb") as wave_file:
                    count = 0
                    data = wave_file.read(FILE_HEADER_SIZE)
                    if self.sending(data):
                        while True:
                            data = wave_file.read(FILE_READ_SIZE)
                            if len(data) == 0:
                                self.sending(b'end')
                                break
                            else:
                                count += 1
                                if not self.sending(data):
                                    break

    def get_data(self):
        data = self.receiving()
        print("len >> {}".format(len(data[3:])))
        print("rec check >> {}".format(data[:3]))
        if data[:3] == b'rec':
            if len(data) > 3:
                # f2.write(data[3:])
                yield data[3:]
            print("go to while")
            while True:
                data = self.receiving()
                if data[-3:] == b'end':
                    if len(data) > 3:
                        yield data[:-3]
                    break
                yield data
