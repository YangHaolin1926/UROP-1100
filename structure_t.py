import json
import os

# 定义转换函数
def convert_book_info(book_info):
    converted_info = {
        "meta": {
            "meta": {
                "meta": {
                "short_book_title": book_info.get("title", ""),
                "publication_date": '',
                "url": book_info.get("url", "")
                }
            }
        },
        "text": book_info.get("text", "")
    }
    return converted_info

# 定义输入和输出文件路径
input_file = os.path.expanduser("~/.cache/huggingface/datasets/downloads.jsonl")
output_file = "/export/project/hyangby/data/book/transferred.jsonl"

# 读取输入文件并转换数据
converted_data = []
with open(input_file, "r") as f:
    for line in f:
        book_info = json.loads(line.strip())
        converted_info = convert_book_info(book_info)
        converted_data.append(converted_info)

# 将转换后的数据存储到输出文件
with open(output_file, "w") as f:
    for converted_info in converted_data:
        f.write(json.dumps(converted_info) + "\n")
