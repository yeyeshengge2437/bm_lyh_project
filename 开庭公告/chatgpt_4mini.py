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
    return output_text


def api_alive_chatgpt():
    url = 'https://ddg-chat-xgh9.onrender.com/ping'
    response = requests.get(url)
    return response.status_code


# print(gpt_freechat(
#     '获取这段信息里的案由，不要输出其他字段：在黑龙江省高级人民法院第六法庭开庭审理上诉人黑龙江省农业融资担保有限责任公司等与被上诉人黑龙江威克特生物科技有限公司等追偿权纠纷上诉案'))

