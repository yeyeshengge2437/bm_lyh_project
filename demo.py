from PIL import Image

# 打开彩色图片文件
color_image = Image.open('20240520213845fd439114b91b4cee.png')

# 转换为黑白模式
black_and_white_image = color_image.convert('L')

# 保存黑白图片
black_and_white_image.save('black_and_white_image.png')

# 如果需要展示图片（在支持图像显示的环境中）
black_and_white_image.show()
