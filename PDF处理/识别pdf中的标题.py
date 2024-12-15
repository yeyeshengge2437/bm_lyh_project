import os
import fitz  # PyMuPDF
import requests
doc = fitz.open("20240521172956e5b115a547754239.pdf")
for page in doc:
    blocks = page.get_text("dict")["blocks"]
    # print(len(blocks))
    for block in blocks:
        try:
            font_type = block["bbox"]
            print(font_type)
            # if font_type == 1:
            #     print(block)
            # if block["lines"][0]["spans"][0]["text"] == "中国中信金融资产管理股份有限公司湖南省分公司与广发银行股份有限公司长沙分行":
            #     print(block)
        except:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            pass
        box_info = block["bbox"]
        rect_annot = fitz.Rect(box_info)  # 使用bbox创建一个矩形
        annot = page.add_rect_annot(rect_annot)

doc.save("new.pdf")
doc.close()
