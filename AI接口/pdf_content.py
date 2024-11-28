import os
import fitz  # PyMuPDF
import requests
import json
import random
import re
import time

from api_ai import img_url_to_file, ai_parse_next, ai_parse_success, ai_parse_fail, pdf_content_except_table_update

def download_pdf(url):
    name = url.split('/')[-1]

    # 发送HTTP GET请求
    response = requests.get(url, stream=True)
    response.raise_for_status()  # 检查请求是否成功

    # 保存文件
    with open(name, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return name


def get_pdf_suspicious_title(page):
    """
    获取疑似为标题的坐标
    :param page:
    :return:
    """
    blocks = page.get_text("dict")["blocks"]
    span_size_num = 0
    count = 0
    for block in blocks:
        try:
            for line in block["lines"]:
                for span in line["spans"]:
                    count += 1
                    # 计算平均span的字体大小
                    size = span["size"]
                    span_size_num += size
        except:
            pass
    average_size = span_size_num / count
    # print(average_size)
    # 如果大于数的百分之50
    location_information = {}
    for block in blocks:
        try:
            for line in block["lines"]:
                for span in line["spans"]:
                    if span["size"] > average_size * 1.5:
                        location = span['bbox']
                        location_information[location] = span['text']

        except:
            pass
    return location_information

def multiple_pages(file_pdf_url):
    """
    AMC中的pdf,没有坐标信息
    :param file_pdf_url:
    :return:
    """
    try:
        file_pdf = download_pdf(file_pdf_url)
    except:
        return "下载失败"
    # 打开PDF文件
    doc = fitz.open(file_pdf)
    tag_str = ''
    # 遍历每一页
    for page in doc:
        # 定位页面上的表格
        tabs = page.find_tables()
        for table in tabs:
            # 对于每个表格中的每个单元格，添加红action注释
            for cell in table.cells:
                # 从单元格的四元组创建矩形对象
                rect = fitz.Rect(cell[0], cell[1], cell[2], cell[3])
                # 添加红action注释到该矩形区域
                page.add_redact_annot(rect)
            # 应用红action注释，删除表格
            page.apply_redactions()

    # 保存修改后的PDF文件
    # doc.save("modified_example.pdf")
    for page in doc:  # 遍历每一页
        text = page.get_text()  # 提取页面文本
        tag_str += text + '\n'  # 将文本添加到字符串中

    # 关闭文档
    doc.close()
    # 删除文件
    if os.path.exists(file_pdf):
        os.remove(file_pdf)
    return tag_str


def single_pages(file_pdf_url, xs, ys, xe, ye, title_sx=0, title_sy=0, title_ex=0, title_ey=0):
    """
    单页pdf,有坐标信息
    :param file_pdf_url:
    :return:
    """
    try:
        file_pdf = download_pdf(file_pdf_url)
    except:
        return "下载失败"
    tag_str = ''
    doc = fitz.open(file_pdf)  # 打开PDF文件
    page = doc[0]
    page_rect = page.rect
    # 获取页面的宽度和高度
    width = page_rect.width
    height = page_rect.height
    x0 = xs * width
    y0 = ys * height
    x1 = xe * width
    y1 = ye * height
    suspicious_title = get_pdf_suspicious_title(page)
    tag_rect = fitz.Rect(x0, y0, x1, y1)
    tabs = page.find_tables(clip=tag_rect)
    for table in tabs:
        # 对于每个表格中的每个单元格，添加红action注释
        for cell in table.cells:
            # 从单元格的四元组创建矩形对象
            rect = fitz.Rect(cell[0], cell[1], cell[2], cell[3])
            # 添加红action注释到该矩形区域
            page.add_redact_annot(rect)
        # 应用红action注释，删除表格
        page.apply_redactions()
    title_text = ''
    if title_sy == 0 and title_ey == 0 and title_sx == 0 and title_ex == 0:
        for location, text in suspicious_title.items():
            print(location, text)
            if (x0 <= location[2]) and (x1 >= location[0]) and (y0 <= location[3]) and (y1 >= location[1]):
                title_text = text
                title_rect = fitz.Rect(location[0], location[1], location[2], location[3])
                # 删除
                page.add_redact_annot(title_rect)
                doc.save("1.pdf")

    else:
        title_rect = fitz.Rect(title_sx * width, title_sy * height, title_ex * width, title_ey * height)
        text = page.get_text(clip=title_rect)
        title_text = text
        # 删除
        page.add_redact_annot(title_rect)
        # 保存新的PDF文件
        # doc.save("1.pdf")


    # 上方区域
    page.add_redact_annot(fitz.Rect(0, 0, width, y0))  # 添加上方区域
    # # 下方区域
    page.add_redact_annot(fitz.Rect(0, y1, width, height))  # 添加下方区域
    # # 左侧区域
    page.add_redact_annot(fitz.Rect(0, y0 - 200, x0, y1 + 200))  # 添加左侧区域
    # # 右侧区域
    page.add_redact_annot(fitz.Rect(x1, y0 - 200, width, y1 + 200))  # 添加右侧区域
    page.apply_redactions()
    # 保存新的PDF文件
    # doc.save("2.pdf")
    # # 保存修改后的PDF文件
    # doc.save("modified_example.pdf")
    text = page.get_text(clip=tag_rect)  # 提取页面文本
    tag_str += text + '\n'
    doc.close()
    if os.path.exists(file_pdf):
        os.remove(file_pdf)
    return tag_str, title_text


# print(single_pages("https://res.debtop.com/manage/live/paper/202408/01/202408010900551ae44f53fec140c1.pdf", 0.008982763,0.753194048, 0.99077446,
#                    0.850142793))

# print(single_pages("https://res.debtop.com/manage/live/paper/202405/31/2024053111032123c32a4ad63d40c7.pdf", 0.499387405,0.572035283, 0.997059544,
#                    0.987095720, 0.635138446, 0.587553087, 0.861308503, 0.600947403))

ai_list = {
    'tell_tool_list': [
        "pdf_content_except_table",
    ]
}

while True:
    try:
        value = ai_parse_next(data=ai_list)
    except:
        time.sleep(360)
        continue
    if value:
        queue_id = value['id']
        input_text = value.get('input_text')
        # 将input_text转换为字典
        input_text = json.loads(input_text)
        qu_id = input_text.get('id')
        pdf_url = input_text.get('pdf_url')
        sx = input_text.get('sx')
        sy = input_text.get('sy')
        ex = input_text.get('ex')
        ey = input_text.get('ey')
        title_sx = input_text.get('title_sx')
        if not title_sx:
            title_sx = 0
        # if title_sx - 0.05 > 0:
        #     title_sx = title_sx - 0.05
        title_sy = input_text.get('title_sy')
        if not title_sy:
            title_sy = 0
        # if title_sy - 0.05 > 0:
        #     title_sy = title_sy - 0.05
        title_ex = input_text.get('title_ex')
        if not title_ex:
            title_ex = 0
        # if title_ex + 0.05 < 1:
        #     title_ex = title_ex + 0.05
        title_ey = input_text.get('title_ey')
        if not title_ey:
            title_ey = 0
        # if title_ey + 0.05 < 1:
        #     title_ey = title_ey + 0.05
        get_info = single_pages(pdf_url, sx, sy, ex, ey, title_sx, title_sy, title_ex, title_ey)
        tag_str, title_text = get_info
        upload_data = {
            'id': qu_id,
            'pdf_title': title_text,
            'content_except_table': tag_str
        }
        print(upload_data)
        pdf_content_except_table_update(data=upload_data)
        success_data = {
            'id': f'{queue_id}',
        }
        ai_parse_success(data=success_data)
        break
    else:
        time.sleep(30)
