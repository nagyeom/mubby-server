# 통신부분에 대한 것을 여기다 모아야 한다.
# 현재는 그냥 동작 돌 수 있도록 가져다 놓았다.
# 추후 수정 필요 꼭
# 커넥팅 후에 꼭!
# 꼬옥!
# 꼭!


class Communication:
    def __init__(self):
        self.sock = None

    def setting_sock(self, sock):
        self.sock = sock

    def sending_wav(self, sock,  audios):
        self.setting_sock(sock)

        with open(audios, "rb") as wave_file:
            count = 0
            data = wave_file.read(44)
            if self.sending(data):
                while True:
                    data = wave_file.read(8192)
                    if len(data) == 0:
                        break
                    else:
                        count += 1
                        print('\t- data len >> ', len(data))
                        print('\t- data count >> ', count)
                        if not self.sending(data):
                            break

    def sending(self, data):
            self.sock.send(data)
            answer = self.sock.recv(1024)
            print('here_re_answer > {}'.format(answer))

            if answer == b'ack':
                return True
            else:
                return False
