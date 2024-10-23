import json
import time

from api_kuake import img_url_identify_fail, img_url_identify_success, get_img_url
from kuake_url import quark

while True:
    value = get_img_url()
    if value is None:
        time.sleep(120)
    id_str = value['id']
    img_url = value['img_url']
    print(img_url)
    identify_data = quark(img_url)
    time.sleep(30)
    identify_code = identify_data['code']
    if identify_code == '00000':
        print('识别成功')
        identify_data = json.dumps(identify_data, ensure_ascii=False)
        data = {
            'id': int(id_str),
            'quark_tables': str(identify_data),
            'remark': '识别成功'
        }
        print(img_url_identify_success(data=data))
    elif identify_code == 'A0401':
        print("图片过大，识别失败")
        data = {
            'id': int(id_str),
            'remark': '图片过大，识别失败'
        }
        print(img_url_identify_fail(data=data))
    else:
        print("识别失败")
        data = {
            'id': int(id_str),
            'remark': f'识别失败,错误码{identify_code}'
        }
        print(img_url_identify_fail(data=data))

