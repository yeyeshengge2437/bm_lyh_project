import os

from PIL import Image

for filename in os.listdir('pdf_images_crop'):
    # 打开图片
    image = Image.open('pdf_images_crop/' + filename)

    # 计算新的图片尺寸
    width, height = image.size
    new_width = width + 2 * 200  # 假设每边留白100像素
    new_height = height  # 假设上下留白50像素

    # 创建一个新的空白图片，背景为白色
    new_image = Image.new('RGB', (new_width, new_height), 'white')

    # 将原图片粘贴到新图片上，居中
    new_image.paste(image, (200, 0))  # (100, 50)是原图片左上角在新图片上的位置

    # 保存或显示新图片
    new_image.save('pdf_images_width_plus/' + filename)
