import json
import random
import re
import time
from multiprocessing import Process
from api_ai import img_url_to_file, ai_parse_next, ai_parse_success, ai_parse_fail
from KIMI import kimi_single_chat, kimi_file_chat
from 智谱 import zhipu_single_chat, zhipu_file_chat, zhipu_file_free_chat
from KIMI_free_api import kimitext_free, kimifile_free
from 跃问 import yuewen_chat, yuewen_file_chat, yuewen_freechat
from qwen import qwentext_free
from chatgpt_4mini import gpt_freechat
from deepseek import deepseek_chat
from character_classificatio import identify_guarantee, identify_mortgagor, identify_collateral
from quark_text import quark_text
from doubao import doubao_pro_32k
from quark_excel import quark_excel
from identify_qrcode import is_qr_code


def text_change(chat_text):
    """
    去除空格、换行符、全角空格、不间断空格
    （目前暂不使用）
    :param chat_text: 对话文字
    :return: 处理后的对话文字
    """
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
        "quark_text",  # quark文字识别
        "doubao_pro_32k",  # doubao文字对话
        "quark_excel",    # quark图片转表格
        "img_code_tell",
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
    'quark_text': quark_text,
    'doubao_pro_32k': doubao_pro_32k,
    'quark_excel': quark_excel,
    'img_code_tell': is_qr_code,
}


def get_ai_value():
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
            # input_text = text_change(input_text)
            try:
                if input_text and file:
                    file_url = json.loads(file)[0]
                    input_token_num, output_token_num, output_text = ai_text_dict[tell_tool](file_url, input_text)
                elif input_text and not file:
                    input_token_num, output_token_num, output_text = ai_text_dict[tell_tool](input_text)
                elif file and not input_text:
                    file_url = json.loads(file)[0]
                    input_token_num, output_token_num, output_text = ai_text_dict[tell_tool](file_url)
                else:
                    fail_data = {
                        'id': f'{queue_id}',
                        'remark': f'传参错误'
                    }
                    print(fail_data)
                    ai_parse_fail(data=fail_data)
                    continue
                if tell_tool == "quark_text":
                    output_text = json.dumps(output_text, ensure_ascii=False)
                    success_data = {
                        'id': queue_id,
                        'remark': name,
                        'output_text': str(output_text),
                    }
                    print('成功', success_data)
                    ai_parse_success(data=success_data)
                else:
                    success_data = {
                        'id': f'{queue_id}',
                        'remark': name,
                        'input_token_num': input_token_num,
                        'output_token_num': output_token_num,
                        'output_text': output_text,
                    }
                    ai_parse_success(data=success_data)
                    print('成功', success_data)
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
            time.sleep(10)


if __name__ == '__main__':
    """
    多进程2个
    """
    process_list = []
    for i in range(2):
        process = Process(target=get_ai_value, args=())
        process_list.append(process)

    for process in process_list:
        process.start()

    for process in process_list:
        process.join()
