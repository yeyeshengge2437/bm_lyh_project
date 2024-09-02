from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import base64
import time


def str_to_binary(s):
    return ''.join(format(ord(c), '08b') for c in s)


def cipher():
    # 获取当前时间戳
    timestamp = int(time.time() * 1000)

    # 生成随机盐
    salt = get_random_bytes(24)

    # 获取当前日期
    year = time.strftime("%Y", time.localtime())
    month = time.strftime("%m", time.localtime()).zfill(2)
    day = time.strftime("%d", time.localtime()).zfill(2)

    # 初始化向量 (IV)
    iv = year + month + day

    # 创建 DES3 加密器
    cipher = DES3.new(salt, DES3.MODE_CBC, iv)

    # 填充数据以符合加密算法的要求
    padded_timestamp = pad(timestamp.to_bytes(8, 'big'), DES3.block_size)

    # 加密数据
    encrypted = cipher.encrypt(padded_timestamp)

    # 将盐、IV 和加密数据合并
    str = salt.hex() + iv + encrypted.hex()

    # 转换为二进制字符串
    ciphertext = str_to_binary(str)

    return ciphertext


# 调用函数并打印结果
ciphertext = cipher()
print(ciphertext)