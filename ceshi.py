import json
from openai import OpenAI

client = OpenAI(
    api_key="sk-ed3b8ed7361c486dbd1baeeb5472c1b7",
    base_url="https://api.deepseek.com",
)

system_prompt = """
用户将提供一些考试文本。请解析 “question” 和 “answer” 并以 JSON 格式输出它们。

EXAMPLE INPUT: 
世界上最高的山是哪座？珠穆朗玛峰。

EXAMPLE JSON OUTPUT:
{
    “question”： 世界上最高的山是哪座？“，
    “answer”： “珠穆朗玛峰”
}
"""

user_prompt = "Which is the longest river in the world? The Nile River."

messages = [{"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}]

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    response_format={
        'type': 'json_object'
    }
)

print(json.loads(response.choices[0].message.content))
