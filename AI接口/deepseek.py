# Please install OpenAI SDK first: `pip3 install openai`
import random

import requests
from openai import OpenAI

# api_key_ren = "sk-e659618a2ea54a09a289ac9861bb61b8"  # 任梁
api_key_liu = "sk-8d54fe4e5cc843978361174a8c0d02c8"  # 刘可恒


def deepseek_chat(chat_text, system_content="您是个乐于助人的助手", temperature=1.0, beta=False):
    api_key = random.Random().choice([api_key_liu])
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

    value = response.json()
    total_balance = value["balance_infos"][0]["total_balance"]
    return total_balance


# print(get_balance(api_key_liu))
# print(deepseek_chat("""
# 从文中提取保证人(担保人默认为保证人, 公司)主体，单个主体以,分割，不要输出其他无关字段（去重）,没有保证人返回'空',智能忽略换行。
# 担保人名称：
# 陆铃、苏锦平
# 上海豪申酒业销售有限公司
# 上海宇醇茶业有限公司"""))
