import os
from openai import OpenAI


# export ARK_API_KEY="9b301c44-9686-43da-9aaa-29feeb4a7e36"

def doubao_pro_32k(chat_text):
    client = OpenAI(
        api_key="9b301c44-9686-43da-9aaa-29feeb4a7e36",
        base_url="https://ark.cn-beijing.volces.com/api/v3",
    )

    # Non-streaming:
    completion = client.chat.completions.create(
        model="ep-20241218200704-qjppf",  # Doubao-pro-32k
        messages=[
            {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
            {"role": "user", "content": f"{chat_text}"},
        ],
    )
    input_token_num = completion.usage.completion_tokens
    output_token_num = completion.usage.prompt_tokens
    output_text = completion.choices[0].message.content
    return input_token_num, output_token_num, output_text


# print(doubao_pro_32k("你好，介绍一下你自己"))
