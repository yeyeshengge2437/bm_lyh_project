# import pdfplumber
# import requests
#
#
# def download_pdf(pdf_url, output_filename):
#     """
#     从给定的链接下载 PDF 文件。
#
#     参数:
#     pdf_url: str, PDF文件的链接。
#     output_filename: str, 下载的PDF文件保存的本地路径。
#     """
#     # 发送 HTTP 请求获取 PDF 文件内容
#     response = requests.get(pdf_url, stream=True)
#
#     # 检查请求是否成功
#     if response.status_code == 200:
#         # 打开一个文件用于写入二进制数据
#         with open(output_filename, 'wb') as f:
#             # 写入从请求中获取的二进制内容
#             f.write(response.content)
#         print(f"PDF 文件已下载为: {output_filename}")
#     else:
#         print('下载失败，状态码:', response.status_code)
#
#
# # 调用函数，传入 PDF 链接和输出文件名
# def down_pdf():
#     pdf_url = 'http://dzb.subaoxw.com/resfiles/2023-03//14//lscm20230314a0004v01.pdf'
#     output_filename = '999.pdf'
#     download_pdf(pdf_url, output_filename)
#     return output_filename
# down_pdf()

# def extract_text(pdf_path):
#     with pdfplumber.open(pdf_path) as pdf:
#         text = ""
#         for page in pdf.pages:
#             text += page.extract_text() + "\n"
#             print(page.extract_text())
#     return text
#
#
#
# # 使用示例
# pdf_path = '999.pdf'
# extracted_text = extract_text(pdf_path)
# # print(extracted_text)

import ddddocr
from PIL import Image
import pdfplumber

# 打开PDF文件
with pdfplumber.open("888.pdf") as pdf:
    for i, page in enumerate(pdf.pages):

        print(page.extract_text())
        # 将PDF页面转换为图像
        img = page.to_image(resolution=500)
        img.save(f"page_{i}.png")
# 获取图片中的文字




