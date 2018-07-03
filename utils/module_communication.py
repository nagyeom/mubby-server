# -*- coding: utf-8 -*-
# from utils.audio_converter import stereo_to_mono

BUF_SIZE = 1024

class Communication:
    def __init__(self):
        self.sock = None
        self.count = 0

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
                        if not self.sending(data):
                            break

    def sending(self, data):
            self.count += 1
            # print('\t- data len >> ', len(data))
            # print('\t- data count >> ', self.count)
            self.sock.send(data)
            answer = self.sock.recv(BUF_SIZE)
            # print('here_re_answer > {}'.format(answer))

            if answer == b'ack':
                return True
            else:
                return False

    def get_data(self, client_recoder):
        # 스트레오 그대로 두고 32000으로 보내면 된다.
        # 파일형식으로 넘길 때는 2채널 스트레오를 모노로 변경해주어야 했는데
        # 다이렉트로 전송은 왠일인지 스트레오로 인식하지 않는다.
        # f1 = open('1channel_record', 'wb')
        f2 = open('2channel_record', 'wb')
        data = client_recoder.recv(BUF_SIZE)
        print("len >> {}".format(len(data[3:])))
        print("rec check >> {}".format(data[:3]))
        if data[:3] == b'rec':
            if len(data) > 3:
                f2.write(data[3:])
                # data = stereo_to_mono(data[3:])
                # f1.write(data)
                yield data[3:]
        print("go to while")
        while True:
            data = client_recoder.recv(BUF_SIZE)
            print("data type >> {}".format(type(data)))
            print("len >> {}".format(len(data)))
            if data[-3:] == b'end':
                if len(data) > 3:
                    f2.write(data[:-3])
                    # data = stereo_to_mono(data[:-3])
                    # f1.write(data)
                    yield data[:-3]
                # f1.close()
                f2.close()
                break
            f2.write(data)
            # data = stereo_to_mono(data)
            # f1.write(data)
            yield data
