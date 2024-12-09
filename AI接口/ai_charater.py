"""
保证人，抵押人/质押人， 保证物/质押物识别
"""
import json
import random
import re
import time
from multiprocessing import Process
from api_ai import img_url_to_file, ai_parse_next, ai_parse_success, ai_parse_fail
from character_classificatio import identify_guarantee, identify_mortgagor, identify_collateral, deepseek_item_guarantee_2, deepseek_item_mortgagor_2


def text_change(chat_text):
    chat_text = re.sub(r'\n', '', chat_text)
    chat_text = re.sub(r' ', '', chat_text)
    chat_text = re.sub(r'\u3000', '', chat_text)
    chat_text = re.sub(r'\xa0', '', chat_text)
    return chat_text


ai_list = {
    'tell_tool_list': [
        "deepseek_item_guarantee",
        "deepseek_item_mortgagor",
        "deepseek_item_collateral",
        "deepseek_item_guarantee_2",
        "deepseek_item_mortgagor_2"
    ]
}
ai_text_dict = {
    "deepseek_item_guarantee": identify_guarantee,  # deepseek-公告债权保证人
    "deepseek_item_mortgagor": identify_mortgagor,  # deepseek-公告债权抵押人
    "deepseek_item_collateral": identify_collateral,  # deepseek-公告债权抵押物
    "deepseek_item_guarantee_2": deepseek_item_guarantee_2,  # deepseek-公告债权保证人-告警处理
    "deepseek_item_mortgagor_2": deepseek_item_mortgagor_2,  # deepseek-公告债权抵押人-告警处理
}


def get_charater_data():
    while True:
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
            remark = value.get('remark')
            if remark:
                if "重复" in remark:
                    fail_data = {
                        'id': f'{queue_id}',
                        'remark': f'重复数据'
                    }
                    print(fail_data)
                    ai_parse_fail(data=fail_data)
                    continue
            # input_text = text_change(input_text)
            if input_text:
                try:
                    if file:
                        file_url = json.loads(file)[0]
                        input_token_num, output_token_num, output_text, prompt = ai_text_dict[tell_tool](file_url, input_text)
                    else:
                        input_token_num, output_token_num, output_text, prompt = ai_text_dict[tell_tool](input_text)
                    success_data = {
                        'id': f'{queue_id}',
                        'remark': name,
                        'input_token_num': input_token_num,
                        'output_token_num': output_token_num,
                        'output_text': output_text,
                        'prompt': prompt
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

            else:
                fail_data = {
                    'id': f'{queue_id}',
                    'remark': f'input_text为空'
                }
                print(fail_data)
                ai_parse_fail(data=fail_data)
        else:
            time.sleep(30)


if __name__ == '__main__':
    """
    多进程5个
    """
    process_list = []
    for i in range(2):
        process = Process(target=get_charater_data, args=())
        process_list.append(process)

    for process in process_list:
        process.start()

    for process in process_list:
        process.join()
