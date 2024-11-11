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
    input_token_num = response['usage']['completion_tokens']
    output_token_num = response['usage']['prompt_tokens']
    output_text = response['choices'][0]['message']['content']
    return input_token_num, output_token_num, output_text


# print(gpt_freechat('输入文字过多，你会怎样'))
