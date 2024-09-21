import pymysql.cursors
import os


def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_IP", "localhost"),
        port=int(os.getenv("DB_PORT", "43306")),
        user="root",
        password="1234",
        database="mnistdb",
    )
