# 选取json文件进行读取
import json
import hashlib


def generate_md5(data):
    """
    生成输入数据的 MD5 哈希值

    参数:
        data: 可以是字符串、字典、列表等

    返回:
        返回数据的 MD5 哈希值（32位十六进制字符串）
    """
    # 如果是字典或列表，先转成 JSON 字符串
    if isinstance(data, (dict, list)):
        data = json.dumps(data, sort_keys=True, ensure_ascii=False)

    # 如果是字符串，编码成字节
    if isinstance(data, str):
        data = data.encode('utf-8')

    # 计算 MD5
    md5_hash = hashlib.md5(data)
    return md5_hash.hexdigest()  # 注意：原代码有拼写错误，应该是 hexdigest()


with open('江阴市国马呢绒染整有限公司.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
for data_key, data_value in data.items():
    if data_value:
        if data_key in ['business_info', 'credit_eval', 'trade_credit']:
            data_md5 = generate_md5(str(data_value))
            pass
            # print(data_key, data_value)
            # 直接上传数据库
        else:
            if 'his_' in data_key:
                # 历史信息，增加标识
                pass
                # print(data_key, data_value)
            else:
                for up_data in data_value:
                    data_md5 = generate_md5(str(up_data))
                    print(data_md5, up_data)
