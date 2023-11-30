import os
import json

# 获取当前路径下的目录名
directory = 'books3'

# 存储文件名的列表
file_names = []

# 遍历目录及其子目录中的文件
for root, dirs, files in os.walk(directory):
    for file in files:
        # 提取文件名部分
        file_name = os.path.splitext(file)[0]
        file_names.append(file_name)

# 存储书籍信息的列表
book_info_list = []

# 读取文件内容并生成书籍信息
for file_name in file_names:
    file_path = os.path.join(directory, file_name + '.txt')
    with open(file_path, 'r') as file:
        content = file.read()

    # 创建书籍信息字典
    book_info = {
        "meta": {
            "meta": {
                "short_book_title": file_name,
                "publication_date": 0,
                "url": ""
            }
        },
        "text": content
    }

    # 将书籍信息添加到列表中
    book_info_list.append(book_info)

# 将书籍信息列表保存到JSONL文件
output_file = 'book_info.jsonl'  # 输出文件名
with open(output_file, 'w') as file:
    for book_info in book_info_list:
        json.dump(book_info, file)
        file.write('\n')

# 打印书籍信息列表
print("书籍信息列表：")
for book_info in book_info_list:
    print(book_info)
