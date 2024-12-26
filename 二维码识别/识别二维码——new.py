from pyzbar.pyzbar import decode
from PIL import Image


def check_qr_code_in_image(image_path):
    try:
        # 使用Pillow库打开图片
        img = Image.open(image_path)
        # 使用pyzbar库解码图片中的二维码
        decoded_objects = decode(img)
        # 如果decoded_objects不为空，说明图片中至少有一个二维码
        if decoded_objects:
            return True
        else:
            return False
    except IOError:
        # 如果图片文件无法打开，返回False
        return False
    except Exception as e:
        # 其他异常，打印异常信息并返回False
        print(f"An error occurred: {e}")
        return False


# print(check_qr_code_in_image("20241024001146dfb219ff6b6f4a8e.png"))
