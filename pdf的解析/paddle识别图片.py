from PIL import Image
from paddleocr import PaddleOCR

# 创建PaddleOCR对象
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

# 正确加载图像文件
img_path = '111.png'
image = Image.open(img_path)  # 使用Pillow库加载图像

# 确保图像被正确加载
if image:
    # 调用OCR函数
    result = ocr.ocr(image, cls=True)
    print(result)
else:
    print(f"无法加载图像: {img_path}")