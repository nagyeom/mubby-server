import pymysql
import os

from datetime import datetime


class MubbyQuery:
    def __init__(self):
        self.host = os.getenv('mysql_host')
        self.user = os.getenv('mysql_user')
        self.password = os.getenv('mysql_password')
        self.db = os.getenv('mysql_db')
        self.charset = 'utf8'

    def connect_mysql(self):
        return pymysql.connect(host=self.host,
                               user=self.user,
                               password=self.password,
                               db=self.db,
                               charset=self.charset)

    def close_mysql(self):
        self.connect_mysql().close()

    def select_tbl_mubby(self):
        """ 무삐 사용자 정보
            0. AUTO INCREMENT
            1. 무삐 일련 번호
            2. 사용자 비밀번호
            3. 무비 별명
            4. 가입 날짜
            5. 최근 접속 날짜
        """
        curs = self.connect_mysql().cursor()

        sql = "select * from tbl_mubby"
        curs.execute(sql)
        return curs.fetchall()

    def select_tbl_message(self):
        """ 무삐 메시지 정보
            0. AUTO INCREMENT
            1. 메시지 내용
            2. 메시지 생성 날짜
            3. 메시지 전송 예약 시간
            4. 답장 내용
            5. 답장 남긴 날짜
            6. 메시지 수신 상태
        """
        curs = self.connect_mysql().cursor()

        sql = "select * from tbl_message"
        curs.execute(sql)
        return curs.fetchall()

# def current_time():
#     now = datetime.now()
#     return now.year, now.month, now.day, now.hour, now.minute, now.second
#
#
# def insert_mubby(curs, conn, serial_no, user_id, user_pw, nickname, join_datetime, rlogin_datetime):
#     data = (serial_no, user_id, user_pw, nickname, join_datetime, rlogin_datetime)
#     sql = """insert into tbl_mubby(serial_no, user_id, user_pw, nickname, join_datetime, rlogin_datetime)
#              values (%s, %s, %s, %s, %s, %s)"""
#     return sql

# serial_no = '1234567'
# user_id = 'test02'
# user_pw = '1234'
# nickname = 'soosang22'
# join_datetime = "{}-{}-{} {}:{}:{}".format(current_time()[0], current_time()[1], current_time()[2],
#                                               current_time()[3], current_time()[4], current_time()[5])
# rlogin_datetime = "{}-{}-{} {}:{}:{}".format(current_time()[0], current_time()[1], current_time()[2],
#                                               current_time()[3], current_time()[4], current_time()[5])

# conn = connect_mysql(host, user )
#
# curs.execute(sql, data)
# conn.commit()
