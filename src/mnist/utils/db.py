import pymysql.cursors
import os


def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_IP", "192.168.0.3"),
        port=int(os.getenv("DB_PORT", "43306")),
        user=os.getenv("DB_USER", "mnist"),
        password=os.getenv("DB_PASSWORD", "1234"),
        database=os.getenv("DB_DATABASE", "mnistdb"),
    )
