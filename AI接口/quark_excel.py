import base64
import random
from time import time
import requests
import json
import uuid
import hashlib
from api_ai import upload_file_by_url

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
        "dataUrl": img_url,
        "dataType": "image",
        "serviceOption": "typeset",
        "inputConfigs": '{"function_option": "excel"}',
        "outputConfigs": "",
        "reqId": req_id,
        "clientId": client_id,
        "signMethod": sign_method,
        "signNonce": sign_nonce,
        "timestamp": timestamp,
        "signature": signature
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
        raise ValueError("Unsupported sign method")
    # 将摘要转换为小写十六进制字符串
    sign = digest.lower()
    return sign


def quark_excel_in(img_url):
    client_id = "test"
    client_secret = "6zGXp1QZ6GcLWoEn"
    http_client = get_http_client()
    param = create_demo_param(client_id, client_secret, img_url)
    req_id = uuid.uuid4().hex
    url = "https://scan-business.quark.cn/vision"
    headers = {
        "Content-Type": "application/json",
    }
    response = http_client.post(url, json=param, headers=headers)
    if response.status_code == 200:
        body = response.json()
        code = body.get("code")
        return body
    else:
        print("http request error")
        return None


def quark_excel(img_url):
    random_num = random.randint(12345, 999999)
    value = quark_excel_in(img_url)
    try:
        filebase64 = value["data"]["TypesetInfo"][0]["FileBase64"]
    except:
        return None
    with open(f"{random_num}.xlsx", "wb") as f:
        f.write(base64.b64decode(filebase64))
    excel_url = upload_file_by_url(random_num, file_type="xlsx")
    return 0, 0, excel_url


print(quark_excel("https://res.debtop.com/manage/live/paper/202410/24/202410240122013548c2b0a7784dd6.png"))
