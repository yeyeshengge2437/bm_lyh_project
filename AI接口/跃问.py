from openai import OpenAI

client = OpenAI(api_key="3jzVuGeNZvuzMYeIz3cYXfdP5T7tUZx7i7DhqtmhQOth8LDA62L4XEHgiQPVx35hT",
                base_url="https://api.stepfun.com/v1")


def yuewen_chat(chat_text):
    completion = client.chat.completions.create(
        model="step-1-8k",
        messages=[
            {
                "role": "system",
                "content": "你是由阶跃星辰提供的AI"
                           "聊天助手，你擅长中文，英文，以及多种其他语言的对话。在保证用户数据安全的前提下，你能对用户的问题和请求，作出快速和精准的回答。同时，你的回答和建议应该拒绝黄赌毒，暴力恐怖主义的内容",
            },
            {"role": "user", "content": f"{chat_text}"},
        ],
    )

    input_token_num = completion.usage.completion_tokens
    output_token_num = completion.usage.prompt_tokens
    output_text = completion.choices[0].message.content
    return input_token_num, output_token_num, output_text


# print(yuewen_chat('你好，请介绍一下阶跃星辰的人工智能!'))

def yuewen_file_chat(img_url, chat_text):
    completion = client.chat.completions.create(
        model="step-1v-8k",
        messages=[
            {
                "role": "system",
                "content": "你是由阶跃星辰提供的AI"
                           "聊天助手，你除了擅长中文，英文，以及多种其他语言的对话以外，还能够根据用户提供的图片，对内容进行精准的内容文本识别。在保证用户数据安全的前提下，你能对用户的问题和请求，作出快速和精准的回答。",
            },
            # 在对话中传入图片，来实现基于图片的理解
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{chat_text}",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"{img_url}"
                        },
                    },
                ],
            },
        ],
    )

    input_token_num = completion.usage.completion_tokens
    output_token_num = completion.usage.prompt_tokens
    output_text = completion.choices[0].message.content
    return input_token_num, output_token_num, output_text


# print(yuewen_file_chat("https://res.debtop.com/manage/live/paper/202410/24/20241024002149e4fba06506cc48b5.png",
#                        "提取里面的文字，不需要总结和概括"))
