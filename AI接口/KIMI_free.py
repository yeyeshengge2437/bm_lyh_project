# -*- coding: utf-8 -*-
# pip install revKimi --upgrade
import os

from revKimi import Chatbot
from api_ai import img_url_to_file
import random

# 定义两个文件的文件名
file1 = './config.json'
file2 = './config_1.json'
file3 = './config_2.json'

# 使用random.choice()从两个文件名中随机选择一个
selected_file = random.choice([file1, file2, file3])

chatbot = Chatbot(config_path=selected_file)


def kimi_file_chat_free(img_file, chat_text):
    file_name = img_url_to_file(img_file)
    with open(file_name, "rb") as f:
        file = f.read()

    resp = chatbot.ask(
        prompt=f"{chat_text}",
        # 提问内容
        conversation_id='',  # 会话ID（不填则会新建）
        # timeout=<timeout>,# 超时时间（默认10秒
        use_search=False,  # 是否使用搜索
        file=file,  # 文件二进制数据（传入代表上传文件）
    )
    if os.path.exists(file_name):
        os.remove(file_name)
    massages = resp['text']
    return 0, 0, massages


def kimi_chat_free(chat_text):
    resp = chatbot.ask(
        prompt=f"{chat_text}",
        # 提问内容
        conversation_id='',  # 会话ID（不填则会新建）
        # timeout=<timeout>,# 超时时间（默认10秒
        use_search=False,  # 是否使用搜索
        # file='',  # 文件二进制数据（传入代表上传文件）
    )
    massages = resp['text']
    return 0, 0, massages


# print(kimi_chat_free('你是谁'))
# print(kimi_file_chat_free('https://res.debtop.com/manage/live/paper/202410/24/20241024001845a058b9867f544a9f.png',
# '提取图片文字'))
