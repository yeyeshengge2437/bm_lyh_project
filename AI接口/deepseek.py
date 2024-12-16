# Please install OpenAI SDK first: `pip3 install openai`
import random

import requests
from openai import OpenAI

# api_key="sk-9a76d51f714449d8b6ff81c74c02a5d0"
api_key_li = "sk-d11beb24cc234b9b9f5df67cee7c69a1"   # 李健
# api_key_zhou = "sk-76f7b57a786e49028921aa98dc677422"   # 周冰


def deepseek_chat(chat_text, system_content="您是个乐于助人的助手", temperature=1.0, beta=False):
    api_key = random.Random().choice([api_key_li])
    if beta:
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/beta")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": f"{chat_text}"},
            ],
            max_tokens=8192,
            temperature=temperature,
            stream=False
        )

        output_token_num = response.usage.completion_tokens
        input_token_num = response.usage.prompt_tokens
        output_text = response.choices[0].message.content
        return input_token_num, output_token_num, output_text
    else:
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": f"{chat_text}"},
            ],
            temperature=temperature,
            stream=False
        )

        output_token_num = response.usage.completion_tokens
        input_token_num = response.usage.prompt_tokens
        output_text = response.choices[0].message.content
        return input_token_num, output_token_num, output_text


# print(deepseek_chat("""你好，介绍一下你自己"""))
def get_balance(token):
    url = "https://api.deepseek.com/user/balance"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


# get_balance(api_key_li)
# print(deepseek_chat("""
# 从文中提取保证人(担保人默认为保证人, 公司)主体，单个主体以,分割，不要输出其他无关字段（去重）,没有保证人返回'空',智能忽略换行。
# 担保人名称：
# 陆铃、苏锦平
# 上海豪申酒业销售有限公司
# 上海宇醇茶业有限公司"""))
