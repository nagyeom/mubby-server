import pymysql


# 연결 되는 동작만 구현
# 추후 DB에 맞게 변경 되어야 한다.
def sql_connection():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        passwd='root',
        db='mysql',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

    return conn


def sql_insert(conn):
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO users (email, password) VALUES(%s, %s)"
            cursor.execute(sql, ('1004@1004.com', 'secret'))

        conn.commit()

    finally:
        conn.close()


def sql_select(conn):
    try:
        with conn.cursor() as cursor:
            sql = "SELECT id, password FROM users WHERE email=%s"
            cursor.execute(sql, ('1004@1004.com',))
            result = cursor.fetchone()
            print(result)

    finally:
        conn.close()


def sql_delete(conn):
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM users WHERE email=%s"
            cursor.execute(sql, ('1004@1004.com',))

        conn.commit()

    finally:
        conn.close()


# 쿼리문이 제대로 동작하는지 확인 할 수 있음.
if __name__ == '__main__':
    # sql_insert(sql_connection())
    # sql_delete(sql_connection())
    sql_select(sql_connection())
