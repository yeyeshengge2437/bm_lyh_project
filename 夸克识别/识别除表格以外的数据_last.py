# from spire.pdf.common import *
# from spire.pdf import *
#
# # 创建一个PdfDocument类的对象
# doc = PdfDocument()
#
# # 加载一个PDF文档
# doc.LoadFromFile("AMC.pdf")
#
# # 将文档转换为HTML
# doc.SaveToFile("PDF转HTML.html", FileFormat.HTML)
# doc.Close()
import os

import fitz  # PyMuPDF
import requests


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


def single_pages(file_pdf_url, xs, ys, xe, ye):
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
    # 上方区域
    page.add_redact_annot(fitz.Rect(0, 0, width, y0))  # 添加上方区域
    # # 下方区域
    page.add_redact_annot(fitz.Rect(0, y1, width, height))  # 添加下方区域
    # # 左侧区域
    page.add_redact_annot(fitz.Rect(0, y0 - 20, x0, y1 + 20))  # 添加左侧区域
    # # 右侧区域
    page.add_redact_annot(fitz.Rect(x1, y0 - 20, width, y1 + 20))  # 添加右侧区域
    page.apply_redactions()
    # 保存新的PDF文件
    doc.save("redacted_area.pdf")
    # # 保存修改后的PDF文件
    # doc.save("modified_example.pdf")
    text = page.get_text(clip=tag_rect)  # 提取页面文本
    tag_str += text + '\n'
    doc.close()
    if os.path.exists(file_pdf):
        os.remove(file_pdf)
    return tag_str


# print(single_pages("https://res.debtop.com/manage/live/paper/202408/01/202408010900551ae44f53fec140c1.pdf", 0.008982763, 0.858560048, 0.99077446,
#                    0.993837367))

# print(single_pages("https://res.debtop.com/manage/live/paper/202408/01/202408010900551ae44f53fec140c1.pdf", 0.008982763,0.753194048, 0.99077446,
#                    0.850142793))

# print(single_pages("https://res.debtop.com/manage/live/paper/202408/01/202408010902001020c214c75d421e.pdf", 0.016142736,0.702871411, 0.983517417,
#                    0.975485189))

# print(single_pages("https://res.debtop.com/manage/live/paper/202408/01/2024080109040054e6470680204496.pdf", 0.025556472,0.76622807, 0.974773289,
#                    0.953070175))

# print(single_pages("https://res.debtop.com/manage/live/paper/202408/01/2024080109040054e6470680204496.pdf", 0.025556472,0.62620614, 0.661665293,
#                    0.760855263))

# print(single_pages("https://res.debtop.com/manage/live/paper/202408/01/20240801090541f3db2f84f7eb4f71.pdf", 0.042435123,0.302230802, 0.679778032,
#                    0.53978979))

# print(single_pages("https://res.debtop.com/manage/live/paper/202408/01/20240801090541f3db2f84f7eb4f71.pdf", 0.68124694,0.448305448, 0.957238453,
#                     0.565744316))

# print(single_pages("https://res.debtop.com/manage/live/paper/202408/01/20240801090541f3db2f84f7eb4f71.pdf", 0.68124694,0.302445302, 0.957238453,
#                     0.447232947))

# print(multiple_pages("https://res.debtop.com/col/live/paper/202410/29/20241029164429a3ec3d9c27704729.pdf"))


# # 打开PDF文件
# doc = fitz.open("paper_xy.pdf")  # 替换为你的PDF文件路径
# page = doc[0]  # 选择第一页，你可以根据需要选择其他页面
# xs = 0.008982763
# xe = 0.99077446
# ys = 0.858560048
# ye = 0.993837367
# # 获取页面尺寸
# page_rect = page.rect
# # 获取页面的宽度和高度
# width = page_rect.width
# height = page_rect.height
# print(width, height)
# x0 = xs * width
# y0 = ys * height
# x1 = xe * width
# y1 = ye * height
# print(x0, y0, x1, y1)
# tag_str = ''
# tag_rect = fitz.Rect(x0, y0, x1, y1)
# tabs = page.find_tables(clip=tag_rect)
# for table in tabs:
#     # 对于每个表格中的每个单元格，添加红action注释
#     for cell in table.cells:
#         # 从单元格的四元组创建矩形对象
#         rect = fitz.Rect(cell[0], cell[1], cell[2], cell[3])
#         # 添加红action注释到该矩形区域
#         page.add_redact_annot(rect)
#     # 应用红action注释，删除表格
#     page.apply_redactions()
#
# doc.save("redacted_area1.pdf")
# redact_rects = [page_rect]  # 初始化红action区域列表，包含整个页面
# # 上方区域
# page.add_redact_annot(fitz.Rect(0, 0, width, y0))  # 添加上方区域
# # # 下方区域
# page.add_redact_annot(fitz.Rect(0, y1, width, height))  # 添加下方区域
# # # 左侧区域
# page.add_redact_annot(fitz.Rect(0, y0, x0, y1))  # 添加左侧区域
# # # 右侧区域
# page.add_redact_annot(fitz.Rect(x1, y0, width, y1))  # 添加右侧区域
# page.apply_redactions()
# # 保存新的PDF文件
# doc.save("redacted_area.pdf")
# # 保存修改后的PDF文件
# # doc.save("modified_example.pdf")
# text = page.get_text(clip=tag_rect)  # 提取页面文本
# tag_str += text + '\n'
# doc.close()


# 未识别成功的文字为矢量图的证据
# import fitz  # 导入PyMuPDF库
#
# # 打开PDF文件
# doc = fitz.open("redacted_area.pdf")
# page = doc[0]
# # 获取页面上的所有矢量图形
# paths = page.get_drawings()
#
# # 打印矢量图形的路径信息
# for path in paths:
#     print(path)
# doc.close()




