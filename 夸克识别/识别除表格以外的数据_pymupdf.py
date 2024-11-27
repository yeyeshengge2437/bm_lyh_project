"""
将pdf中目标位置进行图片保存，使用识别ocr识别目标区域的字符数，后提取pdf中的目标中的字体数，进行文字数对比，如果在文字数在误差的范围内则提取文字。
如果不在误差的范围内，则将目标区域作为图片保存，使用表格识别，利用PIL将表格覆盖，之后利用ai将文本提取。
"""

import fitz


# 打开PDF文件
doc = fitz.open("qqqq.pdf")
# 获取第一页
page = doc[0]



blocks = page.get_text("dict")["blocks"]
titles = []
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
print(average_size)
# 如果大于数的百分之50
for block in blocks:
    try:
        for line in block["lines"]:
            for span in line["spans"]:
                if span["size"] > average_size * 1.5:
                    print(span['bbox'])
                    print(span['text'])
                    # 将其“删除”
                    # 获取位置信息
                    coordinate = span['bbox']
                    rect = fitz.Rect(coordinate[0], coordinate[1], coordinate[2], coordinate[3])
                    # 添加红action注释到该矩形区域
                    page.add_redact_annot(rect)
                    # 应用红action注释，删除表格
        page.apply_redactions()
    except:
        pass
doc.save("new.pdf")
# 关闭文档
doc.close()
