from mnist.worker import get_pr_is_null, update_data, run
from mnist.utils.util import get_now_time
import requests


# def test_get_data():
#     """
#     prediction_result의 값이 None 인지 검증
#     """
#     print(get_now_time())
#     assert get_pr_is_null()
#     assert get_pr_is_null()[6] == None


# def test_update_data():
#     data = get_pr_is_null()
#     print(update_data(data))


# def test_notification():
#     api_url = "https://notify-api.line.me/api/notify"
#     token = "I0oVNunLTcwjnSBJrY21IG0MzyfMG19mSF15KIkfsyg"

#     message_txt = f"""
#     [Worker 알림]
#     Test
#     """

#     headers = {"Authorization": "Bearer " + token}

#     message = {"message": message_txt}

#     try:
#         requests.post(api_url, headers=headers, data=message)
#     except Exception as e:
#         print(e)


def test_run():

    import os

    run()
