from time import time
import requests
import json
import uuid
import hashlib


def get_http_client():
    return requests.session()


def create_demo_param(client_id, client_secret):
    business = "vision"
    sign_method = "SHA3-256"
    sign_nonce = uuid.uuid4().hex
    timestamp = int(time() * 1000)
    signature = get_signature(client_id, client_secret, business, sign_method, sign_nonce, timestamp)
    req_id = uuid.uuid4().hex


    param = {
        "dataUrl": "https://res.debtop.com/col/live/paper/202411/11/202411111710473013e337d6a940c6.png",
        "dataType": "image",
        "serviceOption": "structure",
        "inputConfigs": '{"function_option": "RecognizeTable"}',
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


def main():
    client_id = "test"
    client_secret = "6zGXp1QZ6GcLWoEn"
    http_client = get_http_client()
    param = create_demo_param(client_id, client_secret)
    req_id = uuid.uuid4().hex
    url = "https://scan-business.quark.cn/vision"
    headers = {
        "Content-Type": "application/json",
    }
    response = http_client.post(url, json=param, headers=headers)
    if response.status_code == 200:
        body = response.json()
        code = body.get("code")
        print(body)
        print("ocr request result:", code)
    else:
        print("http request error")


if __name__ == "__main__":
    main()