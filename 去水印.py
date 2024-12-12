import fitz  # PyMuPDF
new_doc = fitz.open()
# 中国长城资产
doc = fitz.open('水印.pdf')
# 获取总页数
page_count = doc.page_count


# 遍历每一页
for page_num in range(page_count):
    page = doc[page_num]
    new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
    # 获取文本
    text_dict = page.get_text("dict")
    blocks = text_dict["blocks"]
    for block in blocks:
        lines = block.get("lines")
        if lines:
            for line in lines:
                for span in line.get("spans"):
                    font = span.get("font")
                    if font == "STSong-Light":
                        pass
                    else:
                        value_text = str(span.get("text"))
                        print(value_text)
                        print(span.get("bbox"))
                        new_page.insert_text((span.get("bbox")[0], span.get("bbox")[1]), value_text, fontsize=span.get("size"), fontname="china-ss")
    # break
new_doc.save("去水印.pdf")
print("11111111111111111")
new_doc.close()
# 关闭源文档
doc.close()
