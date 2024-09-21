from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
import datetime
import os
from fastapi.middleware.cors import CORSMiddleware
import pymysql.cursors

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://food-jh-98.web.app",
        "https://api.samdulshop.shop",
        "https://api.samdulshop.shop/n20",
        "http://localhost",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

username = "n20"


def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_IP", "localhost"),
        port=int(os.getenv("DB_PORT", "43306")),
        user="root",
        password="1234",
        database="mnistdb",
    )


@app.get("/")
def hello():
    return {"msg": "hello"}


def save_db(file, file_name, path, current_time):
    # 데이터베이스에 저장할수 있도록 타임 포맷 지정
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO 
                image_processing (
                                    file_name, 
                                    file_path, 
                                    request_time, 
                                    request_user, 
                                    prediction_model,
                                    prediction_result,
                                    prediction_time
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
            file_path = os.path.join(os.path.dirname(path), file_name)
            cursor.execute(
                sql,
                (
                    file.filename,  # 원본 파일명
                    file_path,  # 저장 전체 경로 및 변환 파일명
                    formatted_time,  # 요청 시간
                    username,  # 요청 사용자
                    "/n20",  # 예측 사용 모델
                    "A",  # 예측 결과
                    "2024-09-20 11:26:30",  # 예측 시간
                ),
            )
        connection.commit()
    except Exception as e:
        print(e)
        return {"error": str(e)}
    finally:
        connection.close()


# 파일 이름, 확장자명, 파일 크기
def get_file_info(): ...


@app.post("/photo")
async def upload_photo(file: UploadFile):

    #  시간 부터 구해야함
    current_time = datetime.datetime.now()
    unix_time = current_time.timestamp()
    upload_f = "./data/images/"

    # 업로드할 파일이 있는지 없는지 검사
    if not os.path.exists(upload_f):
        os.makedirs(upload_f)

    # 업로드된 파일을 읽어 온다.
    content = await file.read()

    # 파일 이름 변형
    t_filename = str(unix_time) + "-" + file.filename
    full_path = os.path.join(os.path.abspath(upload_f), t_filename)

    # 파일 저장
    with open(full_path, "wb") as fp:
        fp.write(content)

    # 데이터 베이스에도 파일에 대한 정보 저장
    save_db(file, t_filename, upload_f, current_time)

    return {
        "file_name": file.filename,
        "file_ext": file.content_type.split("/")[-1],
        "content_type": file.content_type,
        "file_full_path": full_path,
    }


@app.get("/files/")
async def get_files(size: int = 10):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT * 
                FROM image_processing
                ORDER BY request_time DESC
                LIMIT %s
                """
            cursor.execute(sql, size)
            rows = cursor.fetchall()

            # 필드 이름을 키로 매핑하여 데이터를 변환
            result = [
                {
                    "id": row[0],
                    "file_name": row[1],
                    "file_path": row[2],
                    "request_time": row[3],
                    "request_user": row[4],
                    "prediction_model": row[5],
                    "prediction_result": row[6],
                    "prediction_time": row[7],
                }
                for row in rows
            ]
        return {"files": result}
    except Exception as e:
        print(e)
        return {"error": str(e)}
    finally:
        if connection and connection.open:
            connection.close()
