import fitz  # PyMuPDF

# # 打开PDF文件
# doc = fitz.open("20241120-农行、浦发、兴业流水反馈.pdf")
#
# # 删除前95页，注意页面索引从0开始，所以要删除第95页，我们需要指定到第94页
# doc.delete_pages(from_page=0, to_page=94)
#
# # 保存修改后的PDF文件
# doc.save("modified_document.pdf")
#
# # 关闭文档
# doc.close()
doc = fitz.open("modified_document.pdf")


# 遍历文档中的每一页
for page in doc:
    # 获取当前页面的旋转角度
    current_rotation = page.rotation
    # 计算新的旋转角度，向左转90度
    new_rotation = (current_rotation - 90) % 360
    # 设置页面的新旋转角度
    page.set_rotation(new_rotation)

# 保存修改后的PDF文件
doc.save("rotated_document.pdf")

# 关闭文档
doc.close()
