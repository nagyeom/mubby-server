# -*- coding: utf-8 -*-
# from __utils.audio_converter import stereo_to_mono

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
            self.sock.send(data)
            try:
                answer = self.sock.recv(BUF_SIZE)
            except:
                self.sock.close()
                print("close socket")
                return False

            if answer == b'ack':
                return True
            else:
                return False

    def get_data(self, client_recoder):
        f2 = open('2channel_record', 'wb')
        data = client_recoder.recv(BUF_SIZE)
        print("len >> {}".format(len(data[3:])))
        print("rec check >> {}".format(data[:3]))
        if data[:3] == b'rec':
            if len(data) > 3:
                f2.write(data[3:])
                yield data[3:]
        print("go to while")
        while True:
            data = client_recoder.recv(BUF_SIZE)
            if data[-3:] == b'end':
                if len(data) > 3:
                    f2.write(data[:-3])
                    yield data[:-3]
                f2.close()
                break
            f2.write(data)
            yield data
