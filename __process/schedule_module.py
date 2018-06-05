import threading
import sys

from __utils import mysql_connector


sys.setrecursionlimit(1500)

class Scheduling:
    def __init__(self):
        self.tbl_message()
        self.tbl_mubby()

    def tbl_mubby(self):
        rows = mysql_connector.MubbyQuery().select_tbl_mubby()
        for row in rows:
            print(row)
        threading.Timer(5, self.tbl_mubby).start()

    def tbl_message(self):
        rows = mysql_connector.MubbyQuery().select_tbl_message()
        for row in rows:
            print(row)
        threading.Timer(5, self.tbl_message).start()



