# import cv2
#
# image = cv2.imread('qrcode.png')
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
from pyzbar.pyzbar import decode
from PIL import Image


def check_qr_code_in_image(image_path):
    try:
        # 使用Pillow库打开图片
        img = Image.open(image_path)
        # 使用pyzbar库解码图片中的二维码
        decoded_objects = decode(img)
        # 如果decoded_objects不为空，说明图片中至少有一个二维码
        if decoded_objects:
            return True
        else:
            return False
    except IOError:
        # 如果图片文件无法打开，返回False
        return False
    except Exception as e:
        # 其他异常，打印异常信息并返回False
        print(f"An error occurred: {e}")
        return False


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
    try:
        decoded_text = decoded_text[0]
        return decoded_text
    except:
        return None



print(is_qr_code('https://res.debtop.com/manage/live/paper/202410/30/202410300231085e5be76b5ff7457c.png'))
