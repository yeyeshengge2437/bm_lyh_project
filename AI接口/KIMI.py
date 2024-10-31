from pathlib import Path
from openai import OpenAI
from api_ai import img_url_to_fail
import os
client = OpenAI(
        api_key="sk-hXUGUGNz8RN3mgLTUg3n8j0suiBiRnumBJxM1I6giYVYJk7h",
        base_url="https://api.moonshot.cn/v1",
    )

def kimi_file_chat(img_url, chat_text):

    file_name = img_url_to_fail(img_url)

    # 我们支持 pdf, doc 以及图片等格式, 对于图片和 pdf 文件，提供 ocr 相关能力
    file_object = client.files.create(file=Path(file_name), purpose="file-extract")

    # 获取结果
    file_content = client.files.content(file_id=file_object.id).text

    # 把它放进请求中
    messages = [
        {
            "role": "system",
            "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。",
        },
        {
            "role": "system",
            "content": file_content,
        },
        {"role": "user", "content": f"{chat_text}"},
    ]
    if os.path.exists(file_name):
        os.remove(file_name)
    # 然后调用 chat-completion, 获取 Kimi 的回答
    completion = client.chat.completions.create(
        model="moonshot-v1-32k",
        messages=messages,
        temperature=0.3,
    )

    print(completion.choices[0].message.content)
    return completion.choices[0].message.content


# kimi_file_chat(
#     "https://res.debtop.com/manage/live/paper/202410/24/20241024110628f369258f291548b9.png?x-oss-process=image/resize,m_fixed,w_64/quality,Q_5",
#     "提取里面的文字，不需要总结和概括")

def kimi_single_chat(chat_text):

    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system",
             "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
            {"role": "user", "content": f"{chat_text}"}
        ],
        temperature=0.3,
    )

    print(completion.choices[0].message.content)
    return completion.choices[0].message.content


# kimi_single_chat("你好")
