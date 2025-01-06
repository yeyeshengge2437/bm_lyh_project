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
    if count == 0:
        return False
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