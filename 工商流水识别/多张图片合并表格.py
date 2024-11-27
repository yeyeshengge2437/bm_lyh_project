import csv
import os
import time

from 夸克识别.quark_excel import quark_excel
import base64
from openpyxl import Workbook
from io import BytesIO


def file_base64_to_xlsx(base64_str, output_filename):
    # 解码Base64字符串
    binary_data = base64.b64decode(base64_str)
    # 如果Base64编码的是Excel文件，则可以直接保存
    with open(output_filename, 'wb') as f:
        f.write(binary_data)


for root, dirs, files in os.walk('pdf_images_1918张兰娣_rollback'):
    for name in files:
        if "page3_image1" in name:
            print(name)
            # 构建完整的文件路径
            file_path = os.path.join(root, name)
            # 处理文件
            print(file_path, name)
            value = quark_excel(img_path=file_path)
            print(value)
            base64_str = value["data"]["TypesetInfo"][0]["FileBase64"]

            output_filename = name.split('.')[0] + '.xlsx'
            file_base64_to_xlsx(base64_str, f"pdf_image_excel/{output_filename}")
            time.sleep(3)


