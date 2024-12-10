import os

import cv2
from PIL import Image
import fitz  # PyMuPDF
from PIL import Image, ImageEnhance


def save_first_seven_pages(input_pdf, output_pdf, start_page, end_page):
    # 打开原始PDF文件
    doc = fitz.open(input_pdf)
    # 创建一个新的PDF文档
    new_doc = fitz.open()
    # 插入前七页到新文档
    new_doc.insert_pdf(doc, from_page=start_page - 1, to_page=end_page - 1)  # 从第0页到第6页，共7页
    # 保存新文档
    new_doc.save(output_pdf)
    # 关闭文档
    new_doc.close()
    doc.close()


# # 使用示例
# input_pdf = "20241120-农行、浦发、兴业流水反馈.pdf"  # 替换为你的PDF文件路径
# output_pdf = "target_1918张兰娣.pdf"  # 输出文件的路径
# save_first_seven_pages(input_pdf, output_pdf, 25, 50)




# # 使用示例
# pdf_path = "target_1918张兰娣.pdf"  # 替换为你的PDF文件路径
# output_folder = "pdf_images_1918张兰娣"  # 输出图片的文件夹路径
# pdf_to_images(pdf_path, output_folder)


def extract_images_from_pdf(pdf_path, output_folder):
    # 打开PDF文件
    pdf_document = fitz.open(pdf_path)

    # 检查输出文件夹是否存在，如果不存在则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历PDF的每一页
    for current_page in range(len(pdf_document)):
        page = pdf_document.load_page(current_page)  # 加载每一页

        # 获取页面中的所有图片对象
        image_list = page.get_images(full=True)
        for image_index, img in enumerate(image_list):
            xref = img[0]  # 图片的引用
            base_image = pdf_document.extract_image(xref)  # 提取图片信息
            image_bytes = base_image["image"]  # 获取图片的字节信息
            image_ext = base_image["ext"]  # 图片的扩展名
            image_filename = f"page{current_page + 1}_image{image_index + 1}.{image_ext}"
            # 将图片字节信息写入文件
            with open(os.path.join(output_folder, image_filename), "wb") as image_file:
                image_file.write(image_bytes)
            print(f"Extracted {image_filename}")  # 打印提取的图片文件名

    # 关闭PDF文档
    pdf_document.close()


#
# # 使用示例
# pdf_path = "target_1918张兰娣.pdf"  # 替换为你的PDF文件路径
# output_folder = "pdf_images_1918张兰娣"  # 输出图片的文件夹路径
# extract_images_from_pdf(pdf_path, output_folder)


def rotate_images_180_degrees(input_folder, output_folder):
    # 检查输出文件夹是否存在，如果不存在则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        # 检查文件是否是图片
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
            # 打开图片文件
            img_path = os.path.join(input_folder, filename)
            img = Image.open(img_path)

            # 反转图片180度
            img_rotated = img.rotate(90, expand=True)

            # 保存反转后的图片到输出文件夹
            output_path = os.path.join(output_folder, filename)
            img_rotated.save(output_path)
            print(f"Rotated and saved: {output_path}")


# 使用示例
input_folder = "pdf_images_1918张兰娣"  # 替换为你的输入文件夹路径
output_folder = "pdf_images_1918张兰娣_rollback"  # 替换为你的输出文件夹路径
rotate_images_180_degrees(input_folder, output_folder)

# 图片变清晰的步骤
def clarity_image(path_img):
    img = Image.open(path_img)
    enhancer = ImageEnhance.Sharpness(img)
    factor = 10.0  # 增强因子，值越大图像越清晰
    img_enhanced = enhancer.enhance(factor)
    img_enhanced.save(path_img)


# clarity_image("page1_image1.jpeg")

# def usm(img, sigma):
#     # 高斯模糊
#     blur_img = cv2.GaussianBlur(img, (0, 0), sigma)
#     # 混合原始图像和模糊图像
#     usm = cv2.addWeighted(img, 1.5, blur_img, -0.5, 0)
#     return usm
#
#
# # 读取图片
# input_image_path = 'page1_image1.jpeg'  # 替换为你的图片文件路径
# img = cv2.imread(input_image_path)
#
# # 检查图片是否成功读取
# if img is not None:
#     # 应用USM锐化
#     sigma_value = 1  # 你可以调整这个值来控制模糊的程度
#     enhanced_img = usm(img, sigma_value)
#
#     # 保存增强后的图片
#     output_image_path = 'enhanced_image.jpg'  # 输出图片的文件路径
#     cv2.imwrite(output_image_path, enhanced_img)
#
#     # 显示原始图片和增强后的图片
#     cv2.imshow('Original Image', img)
#     cv2.imshow('Enhanced Image', enhanced_img)
#
#     # 等待按键后关闭所有窗口
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
# else:
#     print("Error: Image not found or unable to read.")
def process_image(input_image_path, output_gray_path):
    # 读取图片
    img = cv2.imread(input_image_path)

    # 检查图片是否成功读取
    if img is None:
        print("Error: Image not found or unable to read.")
        return None, None

    # 将图片转换为灰度图
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 保存灰度化和二值化后的图片
    cv2.imwrite(output_gray_path, gray_img)


# # 使用示例
# input_image_path = 'page6_image1.jpeg'  # 替换为你的图片文件路径
# output_gray_path = 'gray_image.jpg'  # 灰度图输出路径
#
# # 调用函数
# gray_img, binary_img = process_image(input_image_path, output_gray_path)

# import numpy as np
#
# # 读取图片
# image = cv2.imread('page1_image1.jpeg')
#
# # 创建拉普拉斯滤波器
# kernel = np.array([[0, -1, 0],
#                    [-1, 5, -1],
#                    [0, -1, 0]])
#
# # 应用滤波器进行锐化
# sharpened = cv2.filter2D(image, -1, kernel)
#
# # 保存结果
# cv2.imwrite('sharpened_text.jpg', sharpened)
