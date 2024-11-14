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

    response = requests.post('https://ddg-chat-ten-jet.vercel.app/v1/chat/completions', headers=headers, json=json_data)
    response = response.content.decode('utf-8')
    response = json.loads(response)
    input_token_num = 0
    output_token_num = 0
    output_text = response['choices'][0]['message']['content']
    return input_token_num, output_token_num, output_text


print(gpt_freechat('\n\n为什么海洋总是很蓝？\n\n因为鱼在里面游泳时总是说：“水真好！”，这个笑话的笑点在哪？'))
