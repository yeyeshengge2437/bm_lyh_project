
import os
import random

import requests
from qreader import QReader
import cv2


def is_qr_code_def(url):
    file_type = url.split('.')[-1]
    file_name = random.randint(12345, 99999)
    res = requests.get(url)
    with open(f'{file_name}.{file_type}', 'wb') as f:
        f.write(res.content)

    qreader = QReader()

    # 获取包含 QR 码的图像
    image = cv2.cvtColor(cv2.imread(f'{file_name}.{file_type}'), cv2.COLOR_BGR2RGB)
    os.remove(f'{file_name}.{file_type}')

    # 使用 detect_and_decode 函数获取解码后的 QR 数据
    decoded_text = qreader.detect_and_decode(image=image)
    if decoded_text:
        return decoded_text
    else:
        return None

