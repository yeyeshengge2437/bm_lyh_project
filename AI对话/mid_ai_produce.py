import re
import time

import requests
from ai_api_mid_produce import ai_parse_next, ai_parse_success, ai_parse_fail


# Authorization: Bearer M3JPM98-JMP46MY-HEF0H3P-CAQED8E

def qwen3_32b(input_text):
    headers = {
        'Content-Type': 'application/json',
    }

    json_data = {
        'model': 'qwen3:32b',
        'prompt': input_text,
        'stream': False,
    }

    response = requests.post('http://localhost:11434/api/generate', headers=headers, json=json_data)
    value_res = response.json()
    answer_str = value_res["response"]
    print(answer_str)
    answer = re.sub(r'<think>.*?</think>', '',  answer_str, flags=re.DOTALL)
    return answer


def deepseekr1_32b(input_text):
    headers = {
        'Content-Type': 'application/json',
    }

    json_data = {
        'model': 'deepseek-r1:32b',
        'prompt': input_text,
        'stream': False,
    }

    response = requests.post('http://localhost:11434/api/generate', headers=headers, json=json_data)
    value_res = response.json()
    answer_str = value_res["response"]
    answer = re.sub(r'<think>.*?</think>', '', answer_str, flags=re.DOTALL)
    return answer






ai_list = {
    'tell_tool_list': [
        'qwen3_32b',
        'deepseekR1_32b'
    ]
}
ai_text_dict = {
    'qwen3_32b': qwen3_32b,
    'deepseekR1_32b': deepseekr1_32b,
}


while True:
    try:
        value = ai_parse_next(data=ai_list)
    except:
        time.sleep(360)
        continue
    if value:
        queue_id = value['id']
        tell_tool = value['tell_tool']
        input_text = value['input_text']
        # input_text = text_change(input_text)
        try:
            answer_str = ai_text_dict[tell_tool](input_text)
            success_data = {
                'id': queue_id,
                'output_text': str(answer_str),
            }
            print('成功', success_data)
            ai_parse_success(data=success_data)
        except Exception as e:
            fail_data = {
                'id': queue_id,
                'remark': f'{e}'
            }
            print(fail_data)
            ai_parse_fail(data=fail_data)
    else:
        time.sleep(30)
