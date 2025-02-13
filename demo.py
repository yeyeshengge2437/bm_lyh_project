from PyPDF2 import PdfReader, PdfWriter


def rotate_odd_pages(input_pdf, output_pdf):
    # 初始化PDF读取器和写入器
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # 遍历每一页
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        # 判断是否为奇数页（页码从1开始，索引从0开始）
        if (page_num + 1) % 2 == 1:
            # 旋转180度（直接设置旋转属性，覆盖原有旋转）
            page.rotate = 180
        # 添加页面到写入器
        writer.add_page(page)

    # 保存处理后的PDF
    with open(output_pdf, 'wb') as out_file:
        writer.write(out_file)


# 示例使用
rotate_odd_pages("农行-万众.pdf", "output——1.pdf")