from datetime import datetime
from mnist.utils.db import get_db_connection
from mnist.utils.util import get_now_time
import random
import requests
import numpy as np
from PIL import Image
from keras.models import load_model
import os

api_url = "https://notify-api.line.me/api/notify"
token = os.getenv("LINE_TOKEN")

file_path = __file__
file_dir = os.path.dirname(file_path)
model_name = "mnist240924.keras"
model_path = os.path.join(file_dir, "mnist240924.keras")
model = load_model(model_path)


# SQL 처리
def execute_sql(sql, params=None, is_commit=False, fetchone=False):
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                if is_commit:
                    connection.commit()
                    return True
                if fetchone:
                    return cursor.fetchone()
    except Exception as e:
        print(f"An error occurred: {e}")
        return False  # 에러 발생 시 False 반환


# Null 인 데이터 하나만 호출
def get_pr_is_null():
    sql = """
        SELECT *
        FROM image_processing
        WHERE prediction_result IS NULL
        LIMIT 1
        """
    return execute_sql(sql, fetchone=True)


def predict_image(image_path):
    img = Image.open(image_path).convert("L")  # 흑백 이미지로 변환
    img = img.resize((28, 28))  # 크기 조정

    # 흑백 반전
    img = np.array(img)  # 흑백 반전

    img = np.array(img)
    img = img.reshape(1, 28, 28, 1)  # 모델 입력 형태에 맞게 변형
    img = img / 255.0  # 정규화

    prediction = model.predict(img)
    digit = np.argmax(prediction)
    return digit


# Null인 데이터 업데이트
def update_data(data):
    idx = data[0]

    digit = predict_image(data[2])

    current_time = get_now_time()

    sql = """
        UPDATE image_processing
        SET prediction_model = %s,
            prediction_result = %s,
            prediction_time = %s
        WHERE num = %s
        """

    params = ("model", digit, current_time, idx)
    if execute_sql(sql, params, is_commit=True):
        return current_time, digit  # 업데이트 성공 시 반환
    else:
        return None, None


# Line 메시지 전송
def send_notification(message_txt):
    headers = {"Authorization": "Bearer " + token}
    message = {"message": message_txt}
    try:
        requests.post(api_url, headers=headers, data=message)
    except Exception as e:
        print(f"Failed to send notification: {e}")


def run():
    """image_processing 테이블을 읽어서 가장 오래된 요청 하나씩을 처리"""

    # STEP 1
    # image_processing 테이블의 prediction_result IS NULL 인 ROW 1 개 조회 - num 갖여오기
    data = get_pr_is_null()

    if data is None:
        # 예외처리
        # 업데이트 할 데이터가 없다면 LINE으로 실패 메시지 전송
        message_txt = "[Worker 알림]\n❌ 업데이트할 데이터가 없습니다. ❌"
        send_notification(message_txt)
    else:

        # STEP 2
        # RANDOM 으로 0 ~ 9 중 하나 값을 prediction_result 컬럼에 업데이트
        # 동시에 prediction_model, prediction_time 도 업데이트
        pr_time, pr_result = update_data(data)
        print(pr_time, pr_result)

        if pr_time is not None:

            # STEP 3
            # LINE 으로 처리 결과 전송
            message_txt = f"""[Worker 알림]\n
🚀  {data[0]}번째의 데이터 Update!
1️⃣  prediction_model : {data[5]} -> {model_name}
2️⃣  tprediction_result : {data[6]} -> {pr_result}
3️⃣  prediction_time : {data[7]} -> {pr_time}
"""
            send_notification(message_txt)
        else:
            print("Failed to update data.")
