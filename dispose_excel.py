def add_newlines(input_file, output_file, chars_per_line=50):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # 将内容分割成单个字符，并添加换行
    new_content = ''
    for i, char in enumerate(content):
        new_content += char
        if (i + 1) % chars_per_line == 0 and i + 1 != len(content):
            new_content += '\n'

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(new_content)

# 使用函数
input_file = '1.txt'  # 需要读取的文件名
output_file = '33.txt'  # 输出文件名
add_newlines(input_file, output_file)
