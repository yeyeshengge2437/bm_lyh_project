import json
import time

from api_ai import img_url_to_file, ai_parse_next, ai_parse_success, ai_parse_fail
from KIMI import kimi_single_chat, kimi_file_chat
from 智谱 import zhipu_single_chat, zhipu_file_chat, zhipu_file_free_chat
from KIMI_free import kimi_chat_free, kimi_file_chat_free
from 跃问 import yuewen_chat, yuewen_file_chat
from qwen import qwentext_free

ai_list = {
    'tell_tool_list': [
        "kimi_8k",
        "kimi_32k",
        "glm_4_air",
        "glm_4v_plus",
        "step-1-8k",  # 跃问文字对话
        "step-1v-8k",  # 跃问文件图片对话
        "qwentext_free",  # 千问免费对话
        "kimi_chat_free",  # kimi免费对话
        "kimi_file_chat_free",  # kimi免费文件对话
    ]
}
ai_text_dict = {
    'kimi_8k': kimi_single_chat,
    'kimi_32k': kimi_file_chat,
    'glm_4_air': zhipu_single_chat,
    'glm_4v_plus': zhipu_file_chat,
    'step-1-8k': yuewen_chat,
    'step-1v-8k': yuewen_file_chat,
    'qwentext_free': qwentext_free,
    'kimi_chat_free': kimi_chat_free,
    'kimi_file_chat_free': kimi_file_chat_free,
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
        if input_text:
            try:
                if file:
                    file_url = json.loads(file)[0]
                    input_token_num, output_token_num, output_text = ai_text_dict[tell_tool](file_url, input_text)
                else:
                    input_token_num, output_token_num, output_text = ai_text_dict[tell_tool](input_text)
                end_time = time.time()
                outcome_time = end_time - start_time
                if outcome_time < 20:
                    time.sleep(20 - outcome_time)
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

        else:
            fail_data = {
                'id': f'{queue_id}',
                'remark': f'input_text为空'
            }
            print(fail_data)
            ai_parse_fail(data=fail_data)
    else:
        time.sleep(30)
