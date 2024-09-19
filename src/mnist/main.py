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


def save_db(file, path):
    print("call save_db")
    current_time = datetime.datetime.now()
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
            
            file_path = os.path.join(os.path.dirname(path), file.filename)
            
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
        print("EXE")
        print(e)
        return {"error": str(e)}
    finally:
        connection.close()


@app.post("/photo")
async def upload_photo(file: UploadFile):
    upload_f = "data/images/"
    if not os.path.exists(upload_f):
        os.makedirs(upload_f)
    
    content = await file.read()
    filename = file.filename
    with open(os.path.join(upload_f, filename), "wb") as fp:
        fp.write(content)

    save_db(file, upload_f)

    return {"filename": filename, "content_type":file.content_type}