import os


def replace_host_in_file(file_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 替换内容
    new_content = content.replace(
        'produce_url = "http://121.43.164.84:29875"',
        'produce_url = "http://118.31.45.18:29875"'
    )

    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)





# 调用函数进行替换
# replace_host_in_file(file_path)

def list_specific_files_in_directory(directory, file_extension):
    # 列出指定目录中的所有文件
    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        if os.path.isfile(full_path) and entry.endswith(file_extension):
            replace_host_in_file(full_path)

# 指定目录路径和文件扩展名
directory_path = '政务公开'
file_extension = '.py'

# 调用函数遍历指定目录中的指定文件
list_specific_files_in_directory(directory_path, file_extension)
