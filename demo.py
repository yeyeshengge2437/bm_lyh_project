import os

from PIL import Image

# # 打开彩色图片文件
# color_image = Image.open('2024102401301999a053971b424897.png')
#
# # 转换为黑白模式
# black_and_white_image = color_image.convert('L')
# # 将图像转换为调色板模式（8位）
# palette_image = black_and_white_image.convert('P', palette=Image.ADAPTIVE)
# # 保存黑白图片
# palette_image.save('black_and_white_image.png', optimize=True)


from PIL import Image
import os


def compress_image(input_path, output_path, max_size_mb=9):
    # 打开图片
    img = Image.open(input_path)

    # 初始化质量参数
    quality = 95  # 从较高的质量开始
    i = 0

    # 循环直到文件大小小于最大大小
    while True:
        # 保存图片
        img.save(f'{output_path}_{i}.jpg', 'JPEG', quality=quality, optimize=True)

        # 检查文件大小
        if os.path.getsize(f'{output_path}_{i}.jpg') <= max_size_mb * 1024 * 1024:
            print(f'Compressed image saved as {output_path}_{i}.jpg')
            return f'{output_path}_{i}.jpg'
        else:
            os.remove(f'{output_path}_{i}.jpg')

        # 如果文件仍然太大，降低质量并重试
        quality -= 5
        i += 1
        if quality < 10:  # 防止质量降到过低
            return None


# 使用示例
# compress_image('2024102401301999a053971b424897.png', 'compress_image.jpg')