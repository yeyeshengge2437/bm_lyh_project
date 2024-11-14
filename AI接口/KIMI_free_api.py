# -*- coding: utf-8 -*-
import requests

refresh_token = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTczOTMyNTk1MCwiaWF0IjoxNzMxNTQ5OTUwLCJqdGkiOiJjc3FsbHZtZ2kzcHRtNm9pdjhuMCIsInR5cCI6InJlZnJlc2giLCJhcHBfaWQiOiJraW1pIiwic3ViIjoiY3NxbDczam12cThrZ2FsajIxODAiLCJzcGFjZV9pZCI6ImNzcWw3M2ptdnE4a2dhbGoyMTdnIiwiYWJzdHJhY3RfdXNlcl9pZCI6ImNzcWw3M2ptdnE4a2dhbGoyMTcwIn0.w404DjOd72w8E8RSaoAxXJxPJ1dc91qjw7cQWp0kuyXgIs7T9_ocuyvjM4W9nBxT-5bCqIXjFfrEASKRYzsm_w'

api_url = 'https://kimi-free-api-vy08.onrender.com/v1/chat/completions'

headers = {
    'Authorization': f'Bearer {refresh_token}',
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
    input_token_num = response['usage']['completion_tokens']
    output_token_num = response['usage']['prompt_tokens']
    output_text = response['choices'][0]['message']['content']
    return input_token_num, output_token_num, output_text


def kimifile_free(img_file_url, chat_text):
    response = get_response_from_api_free(img_file_url, chat_text)
    input_token_num = response['usage']['completion_tokens']
    output_token_num = response['usage']['prompt_tokens']
    output_text = response['choices'][0]['message']['content']
    return input_token_num, output_token_num, output_text


def api_alive():
    url = 'https://kimi-free-api-vy08.onrender.com/ping'
    response = requests.get(url)
    return response.status_code


