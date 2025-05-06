import base64
import os
from time import time
import requests
import json
import uuid
import hashlib
from api_kuake import img_url_to_fail


def get_http_client():
    return requests.session()


def img_to_base64(path):
    with open(path, 'rb') as f:
        base64_data = base64.b64encode(f.read()).decode('utf-8')
    return base64_data


def create_demo_param(client_id, client_secret, img_url):
    business = "vision"
    sign_method = "SHA3-256"
    sign_nonce = uuid.uuid4().hex
    timestamp = int(time() * 1000)
    signature = get_signature(client_id, client_secret, business, sign_method, sign_nonce, timestamp)
    req_id = uuid.uuid4().hex

    param = {
        "clientId": client_id,
        "serviceOption": "structure",
        "inputConfigs": '{"function_option": "RecognizeTable"}',
        "outputConfigs": '{"need_return_image":"True"}',
        "signMethod": sign_method,
        "signNonce": sign_nonce,
        "timestamp": timestamp,
        "dataUrl": img_url,
        "signature": signature,
        "dataType": "image",
        "reqId": req_id,
    }
    return param


def get_signature(client_id, client_secret, business, sign_method, sign_nonce, timestamp):
    raw_str = f"{client_id}_{business}_{sign_method}_{sign_nonce}_{timestamp}_{client_secret}"
    utf8_bytes = raw_str.encode("utf-8")

    # 根据sign_method选择不同的摘要算法
    if sign_method.lower() == "sha256":
        digest = hashlib.sha256(utf8_bytes).hexdigest()
    elif sign_method.lower() == "sha1":
        digest = hashlib.sha1(utf8_bytes).hexdigest()
    elif sign_method.lower() == "md5":
        digest = hashlib.md5(utf8_bytes).hexdigest()
    elif sign_method.lower() in ["sha3-256", "sha3_256"]:
        digest = hashlib.sha3_256(utf8_bytes).hexdigest()
    else:
        raise ValueError("不支持的签名方法")

    # 将摘要转换为小写十六进制字符串
    sign = digest.lower()
    return sign


def quark(img_url):
    client_id = "test"
    client_secret = "6zGXp1QZ6GcLWoEn"

    http_client = get_http_client()
    param = create_demo_param(client_id, client_secret, img_url)
    req_id = uuid.uuid4().hex
    url = "https://scan-business.quark.cn/vision"

    headers = {
        "Content-Type": "application/json",
    }

    response = http_client.post(url, data=json.dumps(param), headers=headers)
    if response.status_code == 200:
        body = response.json()
        try:
            image_info_list = body.get("data").get("ImageInfo")
        except:
            image_info_list = None
        if image_info_list:
            for image_info in image_info_list:
                image_base64 = image_info.get("ImageBase64")
                if image_base64:    # 删除base64信息
                    image_info.pop("ImageBase64")
        code = body.get("code")
        if code != '00000':
            return None
        print(body)
        return body
    else:
        print("HTTP 请求错误")
        return None


# quark('https://res.debtop.com/manage/live/paper/202501/13/20250113201704c27f52cd8d624f2d.png')
