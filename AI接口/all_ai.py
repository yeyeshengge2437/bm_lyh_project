import json
import random
import re
import time

from api_ai import img_url_to_file, ai_parse_next, ai_parse_success, ai_parse_fail
from KIMI import kimi_single_chat, kimi_file_chat
from 智谱 import zhipu_single_chat, zhipu_file_chat, zhipu_file_free_chat
from KIMI_free_api import kimitext_free, kimifile_free
from 跃问 import yuewen_chat, yuewen_file_chat, yuewen_freechat
from qwen import qwentext_free
from chatgpt_4mini import gpt_freechat
from deepseek import deepseek_chat

def text_change(chat_text):
    chat_text = re.sub(r'\n', '', chat_text)
    chat_text = re.sub(r' ', '', chat_text)
    chat_text = re.sub(r'\u3000', '', chat_text)
    chat_text = re.sub(r'\xa0', '', chat_text)
    return chat_text


ai_list = {
    'tell_tool_list': [
        "kimi_8k",
        "kimi_32k",
        "glm_4_air",
        "glm_4v_plus",
        "step_1_8k",  # 跃问文字对话
        "step_1v_8k",  # 跃问文件图片对话
        "yuewentext_free",  # 跃问免费文字对话
        "qwentext_free",  # 千问免费对话
        "kimi_chat_free",  # kimi免费对话
        "kimi_file_chat_free",  # kimi免费文件对话
        "deepseek_chat",  # deepseek文字对话
        "gpt_freechat",  # gpt免费对话 需要搭梯子
    ]
}
ai_text_dict = {
    'kimi_8k': kimi_single_chat,
    'kimi_32k': kimi_file_chat,
    'glm_4_air': zhipu_single_chat,
    'glm_4v_plus': zhipu_file_chat,
    'step-1-8k': yuewen_chat,
    'step-1v-8k': yuewen_file_chat,
    'yuewentext_free': yuewen_freechat,
    'qwentext_free': qwentext_free,
    'kimi_chat_free': kimitext_free,
    'kimi_file_chat_free': kimifile_free,
    'gpt_freechat': gpt_freechat,
    'deepseek_chat': deepseek_chat,
}
while True:
    start_time = time.time()
    try:
        value = ai_parse_next(data=ai_list)
    except:
        time.sleep(360)
        continue
    if value:
        queue_id = value['id']
        name = value['name']
        tell_tool = value['tell_tool']
        input_text = value['input_text']
        file = value.get('files')
        input_text = text_change(input_text)
        if input_text:
            try:
                if file:
                    file_url = json.loads(file)[0]
                    input_token_num, output_token_num, output_text = ai_text_dict[tell_tool](file_url, input_text)
                else:
                    input_token_num, output_token_num, output_text = ai_text_dict[tell_tool](input_text)
                end_time = time.time()
                outcome_time = end_time - start_time
                if 0 < int(outcome_time) < 20:
                    num = random.randint(5, 20)
                    time.sleep(num)
                if "您的账号已达频率限制" in output_text:
                    fail_data = {
                        'id': f'{queue_id}',
                        'remark': f'调用失败,原因:{output_text}'
                    }
                    time.sleep(60)
                    print(fail_data)
                    ai_parse_fail(data=fail_data)
                else:
                    success_data = {
                        'id': f'{queue_id}',
                        'remark': name,
                        'input_token_num': input_token_num,
                        'output_token_num': output_token_num,
                        'output_text': output_text,
                    }
                    print(success_data)
                    ai_parse_success(data=success_data)
            except Exception as e:
                fail_data = {
                    'id': f'{queue_id}',
                    'remark': f'调用失败,原因{e}'
                }
                print(fail_data)
                ai_parse_fail(data=fail_data)
                if "您的账号已达频率限制" in str(e):
                    print('您的账号已达频率限制' + "等待60秒")
                    time.sleep(60)

        else:
            fail_data = {
                'id': f'{queue_id}',
                'remark': f'input_text为空'
            }
            print(fail_data)
            ai_parse_fail(data=fail_data)
    else:
        time.sleep(30)
