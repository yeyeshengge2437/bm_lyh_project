file_path = "extracted_text.txt"  # 假设这是提取PDF文本后的文件路径
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        for char in text:
            try:
                unicode_code = ord(char)
                print(f"字符 {char} 的Unicode编码为: {unicode_code}")
            except TypeError as e:
                print(f"字符 {char} 处理出错: {e}")
except FileNotFoundError as e:
    print(f"文件不存在错误: {e}")
