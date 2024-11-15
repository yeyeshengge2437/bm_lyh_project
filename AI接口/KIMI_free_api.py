# -*- coding: utf-8 -*-
import re
import time

import requests

refresh_token1 = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTczOTQxMzc4MSwiaWF0IjoxNzMxNjM3NzgxLCJqdGkiOiJjc3JiNDVlMGF0cDhmN3M4Zm5wZyIsInR5cCI6InJlZnJlc2giLCJhcHBfaWQiOiJraW1pIiwic3ViIjoiY3NxdjBpbWdpM3B0bTZyYnI0ZTAiLCJzcGFjZV9pZCI6ImNzcXYwaW1naTNwdG02cmJyNGMwIiwiYWJzdHJhY3RfdXNlcl9pZCI6ImNzcXYwaW1naTNwdG02cmJyNGJnIn0.FsHBjkJqK4aw7ikETZiIlrJnZ9y_UEe0DR-a_kzKfxjzTRkJZdIvqe0eySThQTuVQ9is-OdMbdkfrL_cxuJsCQ'
# refresh_token2 = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTczOTQxNjQwNywiaWF0IjoxNzMxNjQwNDA3LCJqdGkiOiJjc3Jib2xxMzRwZTM3cnQ3YnU5ZyIsInR5cCI6InJlZnJlc2giLCJhcHBfaWQiOiJraW1pIiwic3ViIjoiY3NyYmFwNjBhdHA4ZjdzZHIxZGciLCJzcGFjZV9pZCI6ImNzcmJhcDYwYXRwOGY3c2RyMWQwIiwiYWJzdHJhY3RfdXNlcl9pZCI6ImNzcmJhcDYwYXRwOGY3c2RyMWNnIn0.9QhczFVHEqPUOaRMkVWysEJmmk7UU24dXsaYqIBuVdHfhXpu5JOqr5Ub9FKoVVDjqhMjb-v1ozwNtq7GZ3fAmw'
refresh_token3 = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTczOTQyNDY5NSwiaWF0IjoxNzMxNjQ4Njk1LCJqdGkiOiJjc3JkcGR1MGF0cDhmN3UzY2R1MCIsInR5cCI6InJlZnJlc2giLCJhcHBfaWQiOiJraW1pIiwic3ViIjoiY3NyYmFwNjBhdHA4ZjdzZHIxZGciLCJzcGFjZV9pZCI6ImNzcmJhcDYwYXRwOGY3c2RyMWQwIiwiYWJzdHJhY3RfdXNlcl9pZCI6ImNzcmJhcDYwYXRwOGY3c2RyMWNnIn0.20zgmkuUl7U54xgVevARZhopegdet_Qn4K_J6sukUKZYG7czsUAFJZVHvvyIqL-x_YsTxa3aiREWuiKM5xfTZg'
# refresh_token4 = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTczOTM1MTA3NywiaWF0IjoxNzMxNTc1MDc3LCJqdGkiOiJjc3FycTlmZDBwODBpaG5tYWNsZyIsInR5cCI6InJlZnJlc2giLCJhcHBfaWQiOiJraW1pIiwic3ViIjoiY3NxcnE5ZmQwcDgwaWhubWFja2ciLCJzcGFjZV9pZCI6ImNzcXJxOWZkMHA4MGlobm1hY2swIiwiYWJzdHJhY3RfdXNlcl9pZCI6ImNzcXJxOWZkMHA4MGlobm1hY2pnIiwic3NpZCI6IjE3MzEwNzMzMDU4MzYxMzMyMTAiLCJkZXZpY2VfaWQiOiI3NDM3MDU3NjAwNDM0MzE1NTI2In0.9u10fiKGbJHL_YtIsMXcstBK8luuO0mpWOePsDjA4i9OodJ0drpY-EolqjcoNFy34G3_IwAH1-s7oITtUBC3-Q'
refresh_token5 = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTczOTM1Njk3NSwiaWF0IjoxNzMxNTgwOTc1LCJqdGkiOiJjc3F0OGJ1MGF0cDhmN29tcml1ZyIsInR5cCI6InJlZnJlc2giLCJhcHBfaWQiOiJraW1pIiwic3ViIjoiY3NuaWh2dWdpM3B0bTZwOWZmZjAiLCJzcGFjZV9pZCI6ImNzbmlodnVnaTNwdG02cDlmZmVnIiwiYWJzdHJhY3RfdXNlcl9pZCI6ImNzbmlodnVnaTNwdG02cDlmZmUwIn0.XJgVk2hDRQhivQOCONhx4Rh1-USHCjJOeMBr8pe4qeGHap3InvgSBmC3dt07MioTTMZR1Au130By1WQRwnUpEQ'
refresh_token6 = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTczOTM2MzUxOCwiaWF0IjoxNzMxNTg3NTE4LCJqdGkiOiJjc3F1cmZtMGF0cDhmN3M0Z3ZpZyIsInR5cCI6InJlZnJlc2giLCJhcHBfaWQiOiJraW1pIiwic3ViIjoiY3NwZDAzMjM0cGUzN3J2cjAyaGciLCJzcGFjZV9pZCI6ImNzcGQwMzIzNHBlMzdydnIwMmQwIiwiYWJzdHJhY3RfdXNlcl9pZCI6ImNzcGQwMzIzNHBlMzdydnIwMmNnIn0._uHyhHV49eY2g2EDm4SdO95Gd8g-HdYJO2tXY2CHnfvX1YUNEqHM8c2PLmLpqrhFg93EI2xB0hoF-36jiDYE_A'

api_url = 'https://kimi-free-api-vy08.onrender.com/v1/chat/completions'

headers = {
    # 'Authorization': f'Bearer {refresh_token1}, {refresh_token2}, {refresh_token3}, {refresh_token4}',
    'Authorization': f'Bearer {refresh_token1}, {refresh_token3}, {refresh_token5}, {refresh_token6}',
    'Content-Type': 'application/json'
}


def get_response_from_api(user_input):
    data = {

        "model": "kimi",
        # "conversation_id": "cnndivilnl96vah411dg",
        "messages": [
            {
                "role": "user",
                "content": user_input
            }
        ],
        "use_search": False,
        "stream": False
    }
    response = requests.post(api_url, headers=headers, json=data)
    return response.json()


def get_response_from_api_free(img_file_url, user_input):
    data = {
        "model": "kimi",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "file",
                        "file_url": {
                            "url": img_file_url
                        }
                    },
                    {
                        "type": "text",
                        "text": user_input
                    }
                ]
            }
        ],
        "use_search": False
    }
    response = requests.post(api_url, headers=headers, json=data)
    return response.json()


def kimitext_free(chat_text):
    response = get_response_from_api(chat_text)
    print(response)
    input_token_num = 0
    output_token_num = 0
    output_text = response['choices'][0]['message']['content']
    time.sleep(10)
    return input_token_num, output_token_num, output_text


def kimifile_free(img_file_url, chat_text):
    response = get_response_from_api_free(img_file_url, chat_text)
    print(response)
    input_token_num = 0
    output_token_num = 0
    output_text = response['choices'][0]['message']['content']
    time.sleep(10)
    return input_token_num, output_token_num, output_text


def api_alive():
    url = 'https://kimi-free-api-vy08.onrender.com/ping'
    response = requests.get(url)
    return response.status_code


