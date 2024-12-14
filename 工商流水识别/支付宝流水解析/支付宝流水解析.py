import os
import re
import msoffcrypto
import io
import pandas as pd
folder_path = '江阴市欧杨纺织有限公司'
for root, dirs, files in os.walk(folder_path):
    for file in files:
        file_path = os.path.join(root, file)
        # 检查文件扩展名是否为.txt
        if file.endswith('.xlsx') and '支付宝' in file:
            # 匹配密码
            password_value = "".join(re.findall(r"（密码(.*?)）", file))
            # 打开文件
            password = password_value
            # 打开加密的Excel文件
            with open(file_path, 'rb') as f:
                excel = msoffcrypto.OfficeFile(f)
                excel.load_key(password_value)  # 替换为你的密码
                temp = io.BytesIO()
                excel.decrypt(temp)
                temp.seek(0)  # 移动到内存缓冲区的开始位置

            # 使用Pandas读取解密后的Excel文件
            df = pd.read_excel(temp)
            # 保存为新的Excel文件
            df.to_excel(file_path.replace(file, f'{file}_解密.xlsx'), index=False)


