import threading
import sys
import socket

from datetime import datetime
from __utils import mysql_connector


class Scheduling:
    def __init__(self):
        # self.srl = sys.setrecursionlimit(10**6)
        self.ms_conn = mysql_connector.MubbyQuery()
        self.current_time()
        # self.task_tbl_mubby()
        self.task_tbl_message()

        self.HOST = ''
        self.PORT = 50000
        self.ADDR = (self.HOST, self.PORT)
        self.BUFF_SIZE = 1024

    def connect_socket(self):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        clientSocket.connect(self.ADDR)
        return clientSocket

    def current_time(self):
        now = datetime.now()
        return "%04d-%02d-%02d %02d:%02d:00" % (now.year, now.month, now.day, now.hour, now.minute)

    def task_tbl_mubby(self):
        rows = self.ms_conn.select_tbl_mubby()
        for row in rows:
            print("사용자 정보 테이블>>", row)
        threading.Timer(5, self.task_tbl_mubby).start()

    def task_tbl_message(self):
        rows = self.ms_conn.select_tbl_message()
        for row in rows:
            print("사용자 메시지 정보>>", row)
            try:
                if str(row[3])==self.current_time():
                    clientSocket = self.connect_socket()
                    header = 'message'
                    clientSocket.send(header.encode())
                    # ack
                    clientSocket.recv(self.BUFF_SIZE)
                    # send mesage
                    clientSocket.send(row[1].encode())
                    # ack
                    clientSocket.recv(self.BUFF_SIZE)
            except Exception as e:
                print(e)

        threading.Timer(5, self.task_tbl_message).start()

