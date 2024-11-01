import json
from pathlib import Path

from zhipuai import ZhipuAI

client = ZhipuAI(api_key="71af9f1dc48c2e4169dd97e48e4e6623.Hl9rvL7a3hA8kolA")  # 填写您自己的APIKey


def zhipu_file_chat(url, chat_text):
    response = client.chat.completions.create(
        model="glm-4v-plus",  # 填写需要调用的模型名称
        # model="glm-4v",  # 填写需要调用的模型名称
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": url
                        }
                    },
                    {
                        "type": "text",
                        "text": f"{chat_text}"
                    }
                ]
            }
        ]
    )
    input_token_num = response.usage.completion_tokens
    output_token_num = response.usage.prompt_tokens
    output_text = response.choices[0].message.content
    return input_token_num, output_token_num, output_text


# zhipu_file_chat("https://res.debtop.com/manage/live/paper/202410/24/20241024002149e4fba06506cc48b5.png", "提取里面的文字，不需要总结和概括")


def zhipu_single_chat(chat_text):
    """
    GLM-4-AirX	极速推理：具有超快的推理速度和强大的推理效果	8K	4K
    GLM-4-Air	高性价比：推理能力和价格之间最平衡的模型	128K	4K
    GLM-4-FlashX	高速低价：Flash增强版本，超快推理速度。	128K	4K
    GLM-4-Flash	免费调用：智谱AI首个免费API，零成本调用大模型。	128K	4K
    :param chat_text:
    :return:
    """
    response = client.chat.completions.create(
        model="GLM-4-Air",  # 填写需要调用的模型编码
        messages=[
            {"role": "system", "content": "你是一个乐于解答各种问题的助手，你的任务是为用户提供专业、准确、有见地的建议。"},
            {"role": "user",
             "content": f"{chat_text}"}
        ],
    )
    input_token_num = response.usage.completion_tokens
    output_token_num = response.usage.prompt_tokens
    output_text = response.choices[0].message.content
    return input_token_num, output_token_num, output_text


# zhipu_single_chat(111)

def zhipu_file_free_chat(chat_text):
    # 大小：单个文件50M、总数限制为100个文件
    file_object = client.files.create(file=Path("img.png"), purpose="file-extract")

    # 获取文本内容
    file_content = json.loads(client.files.content(file_id=file_object.id).content)["content"]

    # 生成请求消息
    message_content = f"请提取\n{file_content}\n里面的文字"

    response = client.chat.completions.create(
        model="glm-4-long",
        messages=[
            {"role": "user", "content": message_content}
        ],
    )

    input_token_num = response.usage.completion_tokens
    output_token_num = response.usage.prompt_tokens
    output_text = response.choices[0].message.content
    return input_token_num, output_token_num, output_text
