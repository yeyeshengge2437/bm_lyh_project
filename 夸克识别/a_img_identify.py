"""
夸克表格识别
"""
import json
import time
from random import randint
from api_kuake import img_url_identify_fail, img_url_identify_success, get_img_url
from kuake_url import quark
from kuake_base64 import quark_base64

while True:
    try:
        value = get_img_url()
    except:
        time.sleep(30)
        continue
    if not value:
        time.sleep(120)
        continue
    id_str = value['id']
    img_url = value['files']
    img_url = json.loads(img_url)[0]
    print(img_url)
    identify_data = quark(img_url)
    time.sleep(randint(5, 20))
    identify_code = identify_data['code']
    if identify_code == '00000':
        print('识别成功')
        identify_data = json.dumps(identify_data, ensure_ascii=False)
        data = {
            'id': int(id_str),
            'output_text': str(identify_data),
            'remark': '识别成功'
        }
        print(img_url_identify_success(data=data))
    elif identify_code in ['A0401', 'A0406']:
        data = {
            'id': int(id_str),
            'remark': f'压缩图后,识别失败,错误码{identify_code}'
        }
        print(img_url_identify_fail(data=data))
    else:
        print(f"识别失败, 错误码{identify_code}")
        data = {
            'id': int(id_str),
            'remark': f'识别失败,错误码{identify_code}'
        }
        print(img_url_identify_fail(data=data))

