# Please install OpenAI SDK first: `pip3 install openai`
import random

from openai import OpenAI

# api_key="sk-9a76d51f714449d8b6ff81c74c02a5d0"
api_key_li = "sk-d11beb24cc234b9b9f5df67cee7c69a1"
api_key_zhou = "sk-76f7b57a786e49028921aa98dc677422"

api_key = random.Random().choice([api_key_li, api_key_zhou])


def deepseek_chat(chat_text, system_content="您是个乐于助人的助手", temperature=1.0, beta=False):
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
