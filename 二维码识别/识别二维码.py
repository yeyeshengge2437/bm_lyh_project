# import cv2
#
# image = cv2.imread('img_3.png')
# detector = cv2.QRCodeDetector()
# data, vertices_array, binary_qrcode = detector.detectAndDecode(image)
# if data:
#     print("检测到 QR 码，数据:", data)
# else:
#     print("未检测到 QR 码")
import os
import random

import requests
from qreader import QReader
import cv2


def is_qr_code(url):
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
    decoded_text = decoded_text[0]
    return decoded_text

