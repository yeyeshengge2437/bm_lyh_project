import os
import tempfile
from pdf2image import convert_from_path
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter


def split_pdf_page(pdf_path, output_path):
    # 将 PDF 转换为图像
    images = convert_from_path(pdf_path)

    # 为输出 PDF 创建 PdfWriter 对象
    output_pdf = PdfWriter()

    # 创建列表以存储所有图像的各个部分
    img_parts_all = []

    for img in images:
        # 将图像分成 4 个部分
        width, height = img.size
        img_parts = [
            img.crop((0, 0, width // 2, height // 2)),  # 左上
            img.crop((width // 2, 0, width, height // 2)),  # 右上
            img.crop((0, height // 2, width // 2, height)),  # 左下角
            img.crop((width // 2, height // 2, width, height)),  # 右下角
        ]

        # 将此图像的各个部分附加到列表中
        img_parts_all.extend(img_parts)

    # 将每个图像部分转换回 PDF 并将其添加到输出 PDF 中
    for img_part in img_parts_all:
        fd, temp_filename = tempfile.mkstemp(suffix=".pdf")  # 创建新的临时文件
        os.close(fd)  # 关闭文件描述符，我们只需要文件名
        img_part.save(temp_filename, "PDF")  # 将 PIL 图像另存为 PDF
        pdf = PdfReader(temp_filename)  # 加载 PDF 文件
        output_pdf.add_page(pdf.pages[0])  # 将页面添加到输出 PDF 中
        os.remove(temp_filename)  # 删除临时文件

    # 将输出 PDF 写入文件
    with open(output_path, "wb") as f:
        output_pdf.write(f)


# 测试函数
split_pdf_page("pdf1.pdf", "output.pdf")
