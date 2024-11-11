# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

client = OpenAI(api_key="sk-ed3b8ed7361c486dbd1baeeb5472c1b7", base_url="https://api.deepseek.com")

def deepseek_chat(chat_text):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "您是个乐于助人的助手"},
            {"role": "user", "content": f"{chat_text}"},
        ],
        stream=False
    )

    input_token_num = response.usage.completion_tokens
    output_token_num = response.usage.prompt_tokens
    output_text = response.choices[0].message.content
    return input_token_num, output_token_num, output_text


# print(deepseek_chat("""你好，介绍一下你自己"""))
