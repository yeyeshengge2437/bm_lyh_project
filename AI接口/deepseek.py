# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI


def deepseek_chat(chat_text, system_content="您是个乐于助人的助手", temperature=1.0, beta=False):
    if beta:
        client = OpenAI(api_key="sk-9a76d51f714449d8b6ff81c74c02a5d0", base_url="https://api.deepseek.com/beta")
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

        input_token_num = response.usage.completion_tokens
        output_token_num = response.usage.prompt_tokens
        output_text = response.choices[0].message.content
        return input_token_num, output_token_num, output_text
    else:
        client = OpenAI(api_key="sk-9a76d51f714449d8b6ff81c74c02a5d0", base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": f"{chat_text}"},
            ],
            temperature=temperature,
            stream=False
        )

        input_token_num = response.usage.completion_tokens
        output_token_num = response.usage.prompt_tokens
        output_text = response.choices[0].message.content
        return input_token_num, output_token_num, output_text


# print(deepseek_chat("""你好，介绍一下你自己"""))


