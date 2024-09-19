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
        "http://localhost:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

username = "n20"

@app.get("/")
def hello():
    return {"msg":"hello"}


def save_db(file, file_name, path, current_time):
    # 데이터베이스에 저장할수 있도록 타임 포맷 지정
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")


    try:
        connection = pymysql.connect(
            host=os.getenv("DB_IP", "localhost"),
            port=int(os.getenv("DB_PORT", "33306")),
            user='food',
            password='1234',
            database='fooddb'
        )
        with connection.cursor() as cursor:
            sql = "INSERT INTO files (name, path, time, user) VALUES (%s, %s, %s, %s)"
            file_path = os.path.join(os.path.dirname(path), file_name)
            cursor.execute(
                sql, 
                (
                    file.filename,  # 파일 이름
                    file_path,      # 파일 경로
                    formatted_time, # 파일 저장 시간
                    username        # 사용자
                )
            )
        connection.commit()
    except Exception as e:
        print(e)
        return {"error": str(e)}
    finally:
        connection.close()


@app.post("/photo")
async def upload_photo(file: UploadFile):

    #  시간 부터 구해야함
    current_time = datetime.datetime.now()
    unix_time = current_time.timestamp()
    upload_f = "data/images/"

    # 업로드할 파일이 있는지 없는지 검사
    if not os.path.exists(upload_f):
        os.makedirs(upload_f)
    
    # 업로드된 파일을 읽어 온다.
    content = await file.read()

    # 파일 이름 변형
    t_filename = str(unix_time)+"-" + file.filename

    # 파일 저장
    with open(os.path.join(upload_f, t_filename), "wb") as fp:
        fp.write(content)

    # 데이터 베이스에도 파일에 대한 정보 저장
    save_db(file, t_filename, upload_f, current_time)

    return {"filename": file.filename, "content_type":file.content_type}