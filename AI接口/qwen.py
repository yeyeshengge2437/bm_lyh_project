# -*- coding: utf-8 -*-
import requests

# 替换成你的tongyi_sso_ticket  检查 ->> 应用 ->> cookies ->> tongyi_sso_ticket
refresh_token = 'ggywxDKTdSsxMgJm2FHs2YXjpz7K_1vawU*obaGzpf8Gz1g_BynogsOH1apRX0qcdzyjCz$o1Bq30'

api_url = 'https://qwenfreeapi.shadow.cloudns.org/v1/chat/completions'


def get_response_from_api(user_input):
    headers = {
        'Authorization': f'Bearer {refresh_token}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": "step",
        "messages": [
            {
                "role": "user",
                "content": user_input
            }
        ],
        "stream": False
    }
    response = requests.post(api_url, headers=headers, json=data)
    return response.json()


def qwentext_free(chat_text):
    response = get_response_from_api(chat_text)
    input_token_num = response['usage']['completion_tokens']
    output_token_num = response['usage']['prompt_tokens']
    output_text = response['choices'][0]['message']['content']
    return input_token_num, output_token_num, output_text


# print(qwentext_free("你好"))



