import pymysql
from Util.mysql_config import DB_CONFIG


def test_mysql_connection():
    conn = None
    try:
        conn = pymysql.connect(**DB_CONFIG)
        print("MySQL 连接成功")
        return True
    except Exception as e:
        print("MySQL 连接失败:", e)
        return False
    finally:
        if conn:
            conn.close()


def main():
    test_mysql_connection()


if __name__ == "__main__":
    main()