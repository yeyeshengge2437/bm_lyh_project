import re

import fitz  # PyMuPDF


def remove_table(file_path):
    text_all = ""
    table_text = ''
    doc = fitz.open(file_path)  # 打开PDF文件
    for page in doc:  # 遍历每一页
        text = page.get_text()  # 提取页面文本
        # print(text)
        text_all += text
    text_all = re.sub(r'\s', '', text_all)
    print(text_all)

    for i in range(doc.page_count):
        page = doc[i]

        # 检测页面中的表格
        tables = page.find_tables()
        for table in tables:
            # 提取表格内容
            table_data = table.extract()

            # 遍历表格的每一行
            for row in table_data:
                for cell in row:
                    if cell:
                        table_text += cell

    # 关闭文档
    doc.close()
    table_text = re.sub(r'\s', '', table_text)
    print(table_text)
    first_str_num_five = table_text[0:5]
    last_str_num_five = table_text[-5:]
    remove_table_text = re.sub(fr'{first_str_num_five}.*{last_str_num_five}', '', text_all)
    if len(remove_table_text) == len(text_all):
        return False
    else:
        return remove_table_text


print(remove_table("eeee.pdf"))
