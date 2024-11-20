import json

import requests


def gpt_freechat(chat_text):
    headers = {
        'Content-Type': 'application/json',
    }

    json_data = {
        'messages': [
            {
                'role': 'user',
                'content': f'{chat_text}',
            },
        ],
        'model': 'gpt-4o-mini',
        'stream': False,
    }

    response = requests.post('https://ddg-chat-xgh9.onrender.com/v1/chat/completions', headers=headers, json=json_data)
    response = response.content.decode('utf-8')
    response = json.loads(response)
    print(response)
    input_token_num = 0
    output_token_num = 0
    output_text = response['choices'][0]['message']['content']
    return input_token_num, output_token_num, output_text


def api_alive_chatgpt():
    url = 'https://ddg-chat-xgh9.onrender.com/ping'
    response = requests.get(url)
    return response.status_code

# print(gpt_freechat('介绍一下你自己'))
